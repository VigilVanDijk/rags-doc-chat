#!/bin/bash
set -e

# Start Ollama in background
echo "Starting Ollama..."
ollama serve &
OLLAMA_PID=$!

# Function to cleanup on exit
cleanup() {
    echo "Shutting down..."
    kill $OLLAMA_PID 2>/dev/null || true
    exit 0
}

trap cleanup SIGTERM SIGINT

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
for i in {1..30}; do
  if curl -f http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "Ollama is ready!"
    break
  fi
  if [ $i -eq 30 ]; then
    echo "ERROR: Ollama failed to start after 60 seconds"
    exit 1
  fi
  echo "Waiting for Ollama... ($i/30)"
  sleep 2
done

# Pull mistral model (~4GB, good quality, actually exists)
# llama3 is too big (4.6GB), llama3.2:3b is too stupid, llama3.2:7b doesn't exist
echo "Ensuring mistral model is available..."
ollama pull mistral || {
  echo "mistral failed, trying llama3.2:3b as fallback..."
  ollama pull llama3.2:3b || {
    echo "llama3.2:3b failed, falling back to phi3:medium..."
    ollama pull phi3:medium || echo "Warning: All model pulls failed"
  }
}

# Start the API server (this will be the main process)
echo "Starting FastAPI server..."
exec uvicorn api:app --host 0.0.0.0 --port 8000

