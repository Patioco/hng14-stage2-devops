FROM node:20-alpine

WORKDIR /app

# Create non-root user
RUN addgroup -S app && adduser -S app -G app
RUN chown -R app:app /app
USER app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

HEALTHCHECK CMD wget --spider -q http://localhost:3000/health || exit 1

CMD ["node", "app.js"]