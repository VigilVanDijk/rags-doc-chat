# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the app (VITE_API_URL will be set at build time)
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# Production stage
FROM node:20-alpine

WORKDIR /app

# Install serve globally to serve static files
RUN npm install -g serve

# Copy built files from builder
COPY --from=builder /app/dist ./dist

# Expose port (Railway will set PORT env var)
EXPOSE 3000

# Start the server
CMD ["sh", "-c", "serve -s dist -l ${PORT:-3000}"]

