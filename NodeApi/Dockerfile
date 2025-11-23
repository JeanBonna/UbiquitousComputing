# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Copiar arquivos de dependências
COPY package*.json ./
COPY tsconfig.json ./

# Instalar TODAS as dependências (incluindo devDependencies para compilar)
RUN npm install

# Copiar código fonte
COPY src ./src

# Compilar TypeScript para JavaScript
RUN npm run build

# Stage 2: Production
FROM node:20-alpine

WORKDIR /app

# Copiar package.json
COPY package*.json ./

# Instalar APENAS dependências de produção
RUN npm install --omit=dev && npm cache clean --force

# Copiar código compilado do stage anterior
COPY --from=builder /app/dist ./dist

# Expor porta
EXPOSE 3000

# Usuário não-root para segurança
USER node

# Comando de execução
CMD ["node", "dist/server.js"]