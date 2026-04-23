FROM node:18-alpine

WORKDIR /app

# Create non-root user
RUN addgroup -S app && adduser -S app -G app

# Give user ownership of /app
RUN chown -R app:app /app

# Switch to non-root user BEFORE copying package.json
USER app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app
COPY . .

EXPOSE 3000

HEALTHCHECK CMD wget --spider -q http://localhost:3000/health || exit 1

CMD ["node", "app.js"]