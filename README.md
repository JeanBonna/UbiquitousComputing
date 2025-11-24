# 🚀 Sistema de APIs com Gateway e Load Balancing

Projeto de Ubiquitous Computing: Clouds, Iot e Smart Environments - Sistema distribuído com múltiplas APIs e gateway.

---

## 👥 Equipe
- [Jean Bonadeo Dal Santo]
- [Felipe Marostega Fagundes]

---

## 📋 Sobre o Projeto

Sistema com 6 APIs (3 Golang + 3 Node.js), gateway com load balancing, PostgreSQL e testes de carga.

**Características:**
- ✅ Load Balancing (Round-robin)
- ✅ Rate Limiting (30 req/60s)
- ✅ Circuit Breaker
- ✅ 6 instâncias de APIs
- ✅ Gateway em Python (FastAPI)

---

## 🏗️ Arquitetura

```
Cliente → Gateway (porta 8080) → 3 APIs Golang + 3 APIs Node → PostgreSQL
```

---

## 🛠️ Tecnologias

- **Golang** - API REST
- **Node.js/TypeScript** - API REST
- **Python/FastAPI** - Gateway
- **PostgreSQL** - Banco de dados
- **Docker** - Containerização
- **Apache JMeter** - Testes de carga

---

## 🚀 Como Executar

### Pré-requisitos
- Docker e Docker Compose instalados

### Executar o projeto
```bash
docker-compose up --build
```


### Acessar
- **Gateway:** http://localhost:8080

---

## 📡 Endpoints Disponíveis

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/users` | Lista todos os usuários |
| GET | `/users/:id` | Busca usuário por ID |
| POST | `/users` | Cria novo usuário |
| PUT | `/users/:id` | Atualiza usuário |
| DELETE | `/users/:id` | Deleta usuário |

**Monitoramento:**
- `/health` - Status do sistema e circuit breakers

---

## 💾 Portas dos Serviços

| Serviço | Porta |
|---------|-------|
| Gateway (entrada principal) | 8080 |
| Golang APIs | 8081-8083 |
| Node APIs | 3001-3003 |
| PostgreSQL | 5432 |

---

## 🧪 Testes de Carga (JMeter)

### Como executar os testes

1. **Instalar JMeter:** https://jmeter.apache.org/download_jmeter.cgi

2. **Abrir JMeter:**
   ```bash
   jmeter
   ```

3. **Carregar o plano de teste:**
   - File → Open → Selecionar `test-golang-api.jmx` ou `test-node-api.jmx`

4. **Configurar cenário de teste:**
   - Clicar em **Thread Group**
   - Configurar: Number of Threads, Ramp-up Period, Duration

5. **Executar:**
   - Run → Start (ou clique no botão ▶️)

6. **Ver resultados:**
   - Summary Report
   - Aggregate Report

### Cenários de Teste

| Cenário | Threads | Ramp-up | Duration |
|---------|---------|---------|----------|
| **Carga Normal** | 50 | 30s | 300s |
| **Estresse** | 200 | 60s | 180s |

---

## 📊 Resultados

Os resultados detalhados dos testes de carga e estresse, incluindo análises comparativas de performance entre as APIs e comportamento do sistema sob diferentes cargas, estão disponíveis no **artigo técnico** que acompanha este projeto.

---

## 🛡️ Features do Gateway

- **Load Balancing:** Distribui requisições entre as 6 APIs usando round-robin
- **Rate Limiting:** Limita a 30 requisições por minuto por IP
- **Circuit Breaker:** Detecta APIs com falhas e desvia o tráfego automaticamente
- **Monitoramento:** Endpoints de health check e métricas em tempo real

---

## 🛑 Parar o Projeto

```bash
docker-compose down
```