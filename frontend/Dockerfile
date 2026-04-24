# ---- Build stage ----
FROM node:18-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# ---- Runtime stage ----
FROM node:18-alpine
WORKDIR /app

RUN adduser -D app
USER app

COPY --from=builder /app/dist ./dist

EXPOSE 3000

HEALTHCHECK CMD wget --spider -q http://localhost:3000/health || exit 1

CMD ["node", "dist/server.js"]