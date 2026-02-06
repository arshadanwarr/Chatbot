import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings and configuration"""
    
    # API Settings
    API_TITLE = "AI Chatbot API"
    API_VERSION = "1.0.0"
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    
    # Ollama Settings
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama2")
    
    # Available models
    AVAILABLE_MODELS = [
        "llama2",
        "mistral",
        "codellama",
        "neural-chat",
        "phi",
        "orca-mini"
    ]
    
    # Memory Settings
    MAX_MEMORY_MESSAGES = int(os.getenv("MAX_MEMORY_MESSAGES", 100))
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", 60))
    RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", 60))  # seconds
    
    # Session Settings
    SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", 3600))  # 1 hour
    MAX_ACTIVE_SESSIONS = int(os.getenv("MAX_ACTIVE_SESSIONS", 100))
    
    # CORS Settings
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Redis (optional for persistent sessions)
    REDIS_URL = os.getenv("REDIS_URL", None)
    USE_REDIS = os.getenv("USE_REDIS", "false").lower() == "true"

settings = Settings()