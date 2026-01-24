# Docker Deployment Guide

This project uses a single Dockerfile that runs both Ollama (LLM) and the FastAPI backend in one container.

## Building the Docker Image

```bash
docker build -t gojira-rag-chat .
```

## Running Locally with Docker

```bash
docker run -p 8000:8000 -p 11434:11434 \
  -v $(pwd)/gojiraDB:/app/gojiraDB \
  -v $(pwd)/data:/app/data \
  gojira-rag-chat
```

The container will:
1. Start Ollama service
2. Wait for Ollama to be ready
3. Pull llama3 model (if not already present)
4. Start the FastAPI server on port 8000

## Environment Variables

You can customize the deployment with environment variables:

- `OLLAMA_BASE_URL`: Ollama service URL (default: `http://localhost:11434`)
- `CORS_ORIGINS`: Comma-separated list of allowed frontend origins (default: localhost URLs)

Example:
```bash
docker run -p 8000:8000 \
  -e CORS_ORIGINS="https://your-frontend.com,https://www.your-frontend.com" \
  gojira-rag-chat
```

## Testing

Once the container is running:

```bash
# Health check
curl http://localhost:8000/health

# Test query
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How many songs are in The Link?"}'
```

## Deployment to Cloud Platforms

### Railway
1. Push code to GitHub
2. Connect repository to Railway
3. Railway will detect Dockerfile and build automatically
4. Set environment variables in Railway dashboard
5. Deploy!

### Render
1. Push code to GitHub
2. Create new Web Service in Render
3. Connect your repository
4. Render will use the Dockerfile
5. Set environment variables
6. Deploy!

### Fly.io
```bash
# Install flyctl
# Login
fly auth login

# Launch app
fly launch

# Deploy
fly deploy
```

## Notes

- The Chroma DB (`gojiraDB/`) should be persisted via volume mounts
- Ollama models are stored in the container - consider using volumes for persistence
- First startup may take time to download the llama3 model (~4GB)

