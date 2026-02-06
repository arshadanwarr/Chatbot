<<<<<<< HEAD
# Chatbot
AI Chatbot with logic, backend and frontend. Using Langchain, Ollama, FastAPi, HTML/CSS.
=======
# AI Chatbot with LangChain, Ollama & FastAPI

A full-featured conversational AI chatbot with memory, built using LangChain, Ollama, and FastAPI backend.

## 🚀 Features

### Core Features
- ✅ **Conversational Memory** - Maintains context across messages
- ✅ **Multiple Sessions** - Support for concurrent user sessions
- ✅ **REST API** - Complete RESTful API with FastAPI
- ✅ **WebSocket Support** - Real-time bidirectional communication
- ✅ **Session Management** - Create, list, and delete chat sessions
- ✅ **Conversation History** - Retrieve and clear chat history
- ✅ **Configurable Models** - Switch between different Ollama models
- ✅ **Temperature Control** - Adjust response creativity
- ✅ **CORS Enabled** - Ready for frontend integration

### Advanced Features
- 🔹 Context awareness and topic tracking
- 🔹 User preferences storage
- 🔹 Health check endpoint
- 🔹 Streaming responses
- 🔹 Error handling and validation
- 🔹 Async/await support
- 🔹 Rate limiting ready
- 🔹 Redis support for persistent sessions (optional)

## 📋 Prerequisites

1. **Python 3.8+**
2. **Ollama** - Install from [ollama.ai](https://ollama.ai)

## 🛠️ Installation

### 1. Install Ollama

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Or download from https://ollama.ai/download
```

### 2. Pull an Ollama Model

```bash
# Pull the default model (llama2)
ollama pull llama2

# Or other models
ollama pull mistral
ollama pull codellama
ollama pull phi
```

### 3. Clone and Setup Project

```bash
# Create project directory
mkdir chatbot-project
cd chatbot-project

# Copy all the provided files into this directory

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configuration

```bash
# Copy environment example
cp .env.example .env

# Edit .env file as needed (optional)
nano .env
```

## 🚀 Running the Application

### Start Ollama Server

```bash
# Make sure Ollama is running
ollama serve
```

### Start FastAPI Backend

```bash
# Run the server
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc

## 💬 Usage

### Option 1: Using the Python Client

```bash
# Start interactive chat
python client.py

# With custom session
python client.py --session my-session-123

# With custom API URL
python client.py --url http://localhost:8000
```

### Option 2: Using WebSocket Client

```bash
# Start real-time chat
python websocket_client.py

# With custom parameters
python websocket_client.py --session ws-session --url ws://localhost:8000
```

### Option 3: Using cURL

```bash
# Send a message
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! Tell me about yourself.",
    "session_id": "user123",
    "temperature": 0.7
  }'

# Get conversation history
curl -X GET "http://localhost:8000/api/history/user123"

# Clear history
curl -X DELETE "http://localhost:8000/api/clear/user123"

# List all sessions
curl -X GET "http://localhost:8000/api/sessions"
```

### Option 4: Using Python Requests

```python
import requests

# Send message
response = requests.post(
    "http://localhost:8000/api/chat",
    json={
        "message": "What is machine learning?",
        "session_id": "python-client",
        "temperature": 0.7,
        "max_tokens": 2000
    }
)

print(response.json()["response"])
```

## 📡 API Endpoints

### Chat Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Send message and get response |
| GET | `/api/history/{session_id}` | Get conversation history |
| DELETE | `/api/clear/{session_id}` | Clear conversation history |

### Session Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/sessions` | List all active sessions |
| DELETE | `/api/sessions/{session_id}` | Delete a session |

### WebSocket

| Protocol | Endpoint | Description |
|----------|----------|-------------|
| WS | `/ws/{session_id}` | Real-time chat connection |

### Utility

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/api/health` | Health check |

## 📚 API Documentation

### Chat Request

```json
{
  "message": "Your message here",
  "session_id": "unique-session-id",
  "temperature": 0.7,
  "max_tokens": 2000
}
```

### Chat Response

```json
{
  "response": "Bot response here",
  "session_id": "unique-session-id",
  "timestamp": "2024-02-04T10:30:00",
  "metadata": {
    "session_id": "unique-session-id",
    "message_count": 5,
    "topics": ["machine", "learning"]
  }
}
```

## 🎛️ Configuration Options

### Environment Variables

```bash
# API Settings
API_HOST=0.0.0.0
API_PORT=8000

# Ollama Settings
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=llama2

# Memory Settings
MAX_MEMORY_MESSAGES=100

# Session Settings
SESSION_TIMEOUT=3600
MAX_ACTIVE_SESSIONS=100
```

### Available Models

- `llama2` - General purpose (default)
- `mistral` - Fast and capable
- `codellama` - Code generation
- `phi` - Lightweight
- `neural-chat` - Conversational
- `orca-mini` - Compact model

## 🔧 Advanced Usage

### Changing Models

```python
# In your chatbot instance
chatbot.change_model("mistral")
```

### Adjusting Temperature

```python
# Higher temperature = more creative
response = client.send_message(
    "Write a story",
    temperature=0.9
)

# Lower temperature = more focused
response = client.send_message(
    "What is 2+2?",
    temperature=0.1
)
```

### Getting Conversation Summary

```python
summary = chatbot.get_summary()
print(summary)
```

## 🧪 Testing

```bash
# Install testing dependencies
pip install pytest httpx

# Run tests (if test file is created)
pytest tests/
```

## 📊 Project Structure

```
chatbot-project/
├── main.py                 # FastAPI application
├── chatbot.py             # ChatBot class with LangChain
├── models.py              # Pydantic models
├── config.py              # Configuration settings
├── client.py              # REST API client
├── websocket_client.py    # WebSocket client
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables example
└── README.md             # This file
```

## 🎯 Use Cases

1. **Customer Support Bot** - Handle customer queries with context
2. **Personal Assistant** - Task management and information retrieval
3. **Educational Tutor** - Interactive learning with memory
4. **Code Helper** - Programming assistance with context
5. **Creative Writing Partner** - Collaborative story/content creation

## 🔐 Security Considerations

- Add authentication for production use
- Implement rate limiting
- Validate and sanitize inputs
- Use HTTPS in production
- Secure WebSocket connections
- Set proper CORS origins

## 🐛 Troubleshooting

### Ollama Connection Error

```bash
# Make sure Ollama is running
ollama serve

# Check if model is downloaded
ollama list
```

### Module Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Port Already in Use

```bash
# Change port in .env or command
uvicorn main:app --port 8001
```

## 📈 Performance Tips

1. Use smaller models (phi, orca-mini) for faster responses
2. Limit conversation history length
3. Adjust `max_tokens` based on needs
4. Use Redis for production session management
5. Enable caching for repeated queries

## 🤝 Contributing

Feel free to extend this chatbot with:
- Database integration (PostgreSQL, MongoDB)
- Authentication & authorization
- Rate limiting
- Caching layer (Redis)
- Frontend interface (React, Vue)
- Voice input/output
- Multi-language support
- Sentiment analysis
- Intent recognition

## 📄 License

MIT License - feel free to use and modify!

## 🙏 Acknowledgments

- [LangChain](https://python.langchain.com/) - LLM framework
- [Ollama](https://ollama.ai/) - Local LLM runtime
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review Ollama documentation
3. Check LangChain documentation
4. Review FastAPI documentation

---

**Happy Chatting! 🤖💬**
>>>>>>> fa30b88 (Initial commit)
