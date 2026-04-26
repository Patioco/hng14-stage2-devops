FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install --omit=dev

FROM node:20-alpine
WORKDIR /app

RUN addgroup -S app && adduser -S app -G app
USER app

COPY --from=builder /app/node_modules ./node_modules
COPY . .

HEALTHCHECK CMD wget --spider -q http://localhost:3000 || exit 1

CMD ["node", "app.js"]