# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Ollama

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Or download from https://ollama.ai/download
```

### Step 2: Pull a Model

```bash
ollama pull llama2
```

### Step 3: Run Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

### Step 4: Start Ollama (in a separate terminal)

```bash
ollama serve
```

### Step 5: Start the API

```bash
source venv/bin/activate  # Activate virtual environment
python main.py
```

### Step 6: Test It!

**Option A: Use the Python Client**
```bash
python client.py
```

**Option B: Use the Web Interface**
- Open `frontend.html` in your browser

**Option C: Use cURL**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "session_id": "test"}'
```

## 📝 Common Commands

```bash
# Start the API
python main.py

# Run tests
pytest test_api.py

# Interactive chat
python client.py

# WebSocket chat
python websocket_client.py

# With Docker
docker-compose up -d
```

## 🔧 Troubleshooting

**Problem**: "Connection refused to Ollama"
**Solution**: Make sure Ollama is running with `ollama serve`

**Problem**: "Module not found"
**Solution**: Activate virtual environment with `source venv/bin/activate`

**Problem**: "Port 8000 already in use"
**Solution**: Change the port in `.env` file or kill the process using that port

## 📚 Learn More

- Check the full README.md for detailed documentation
- Visit API docs at http://localhost:8000/docs
- Ollama models: https://ollama.ai/library

## 🎯 Next Steps

1. Try different Ollama models (mistral, codellama, phi)
2. Build a custom frontend
3. Add database persistence
4. Implement authentication
5. Deploy to production

Happy chatting! 🤖