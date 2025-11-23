import os
import itertools
import time
from collections import deque, defaultdict
from datetime import datetime, timedelta
from typing import List
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
import httpx

# ---------- Config ----------
UPSTREAMS = [
    u.strip().rstrip("/") 
    for u in os.getenv("UPSTREAMS", "http://api1:8080,http://api2:8080").split(",") 
    if u.strip()
]
RATE_LIMIT = int(os.getenv("RATE_LIMIT", "30"))
WINDOW_SEC = int(os.getenv("WINDOW_SEC", "60"))
CB_FAIL_THRESHOLD = int(os.getenv("CB_FAIL_THRESHOLD", "3"))
CB_COOLDOWN_SEC = int(os.getenv("CB_COOLDOWN_SEC", "10"))

# ---------- App ----------
app = FastAPI(title="Golang API Gateway", docs_url="/_docs")

# Rate limit (per IP)
_recent = defaultdict(deque)  # ip -> timestamps
_window = timedelta(seconds=WINDOW_SEC)

# Round-robin
_rr = itertools.cycle(range(len(UPSTREAMS)))

# Circuit breaker per upstream
# state: "closed" | "open" | "half"
_cb = {
    i: {"state": "closed", "fail": 0, "opened_at": 0.0}
    for i in range(len(UPSTREAMS))
}

def _client_ip(req: Request) -> str:
    """Extract client IP from request"""
    fwd = req.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    return req.client.host or "?"

def _rate_limit(ip: str) -> bool:
    """Check if IP has exceeded rate limit"""
    now = datetime.utcnow()
    q = _recent[ip]
    
    # Remove old timestamps outside the window
    while q and (now - q[0]) > _window:
        q.popleft()
    
    # Check if limit exceeded
    if len(q) >= RATE_LIMIT:
        return True
    
    # Add current timestamp
    q.append(now)
    return False

def _pick_upstream_index() -> int:
    """Pick next upstream using round-robin, respecting circuit breaker state"""
    # Keep picking until one is not OPEN (allow half/closed)
    for _ in range(len(UPSTREAMS)):
        i = next(_rr)
        st = _cb[i]
        
        if st["state"] == "open":
            # Allow half-open if cooldown passed
            if (time.time() - st["opened_at"]) >= CB_COOLDOWN_SEC:
                st["state"] = "half"
                return i
            # else skip
            continue
        
        return i
    
    # If all open and still cooling, raise error
    raise HTTPException(
        status_code=503, 
        detail="No healthy upstreams (circuit open)"
    )

def _on_success(i: int):
    """Mark upstream as successful"""
    st = _cb[i]
    st["fail"] = 0
    st["state"] = "closed"

def _on_failure(i: int):
    """Mark upstream as failed and update circuit breaker"""
    st = _cb[i]
    st["fail"] += 1
    
    # Open circuit if in half-open state or threshold reached
    if st["state"] == "half" or st["fail"] >= CB_FAIL_THRESHOLD:
        st["state"] = "open"
        st["opened_at"] = time.time()

# Hop-by-hop headers that should not be forwarded
HOP = {
    "connection", "keep-alive", "proxy-authenticate", 
    "proxy-authorization", "te", "trailers", 
    "transfer-encoding", "upgrade"
}

@app.middleware("http")
async def limit(req: Request, call_next):
    """Rate limiting middleware"""
    if _rate_limit(_client_ip(req)):
        raise HTTPException(
            status_code=429, 
            detail=f"Rate limit exceeded ({RATE_LIMIT}/{WINDOW_SEC}s)"
        )
    return await call_next(req)

@app.api_route(
    "/{path:path}", 
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]
)
async def proxy(req: Request, path: str):
    """Main proxy endpoint - forwards requests to upstreams"""
    # Pick upstream
    i = _pick_upstream_index()
    upstream = UPSTREAMS[i]
    
    # Build URL
    url = f"{upstream}/" + (path or "")
    if req.url.query:
        url += f"?{req.url.query}"
    
    # Read request body
    body = await req.body()
    
    # Filter hop-by-hop headers
    headers = {k: v for k, v in req.headers.items() if k.lower() not in HOP}
    
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=False) as c:
            r = await c.request(
                req.method, 
                url, 
                headers=headers, 
                content=body
            )
    except Exception as e:
        _on_failure(i)
        raise HTTPException(
            status_code=502, 
            detail=f"Bad gateway (upstream error): {str(e)}"
        )
    
    # Treat 500+ as failure for circuit breaker
    if r.status_code >= 500:
        _on_failure(i)
    else:
        _on_success(i)
    
    # Filter response headers
    resp_headers = {k: v for k, v in r.headers.items() if k.lower() not in HOP}
    
    return Response(
        content=r.content, 
        status_code=r.status_code, 
        headers=resp_headers, 
        media_type=r.headers.get("content-type")
    )

@app.get("/_health")
def health():
    """Health check endpoint - shows gateway status"""
    return {
        "upstreams": UPSTREAMS,
        "circuit_breakers": _cb,
        "rate_limit": RATE_LIMIT,
        "window_seconds": WINDOW_SEC,
        "status": "healthy"
    }

@app.get("/_metrics")
def metrics():
    """Metrics endpoint - shows detailed statistics"""
    active_clients = len(_recent)
    total_requests = sum(len(q) for q in _recent.values())
    
    cb_status = []
    for i, cb in _cb.items():
        cb_status.append({
            "upstream": UPSTREAMS[i],
            "state": cb["state"],
            "failures": cb["fail"],
            "opened_at": cb["opened_at"] if cb["opened_at"] > 0 else None
        })
    
    return {
        "active_clients": active_clients,
        "total_requests_in_window": total_requests,
        "circuit_breakers": cb_status,
        "config": {
            "rate_limit": RATE_LIMIT,
            "window_seconds": WINDOW_SEC,
            "cb_fail_threshold": CB_FAIL_THRESHOLD,
            "cb_cooldown_seconds": CB_COOLDOWN_SEC
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)