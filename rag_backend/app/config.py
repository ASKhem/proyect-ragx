from environs import Env

env = Env()
env.read_env()

class Settings:
    API_KEY = env.str("NVIDIA_API_KEY")
    BASE_URL = "https://integrate.api.nvidia.com/v1"
    MODEL_NAME = "nvidia/llama-3.1-nemotron-70b-instruct"
    
    # MongoDB settings
    MONGODB_URL = env.str("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_USER = env.str("MONGODB_USER", "")
    MONGODB_PASSWORD = env.str("MONGODB_PASSWORD", "")
    MONGODB_AUTH_SOURCE = env.str("MONGODB_AUTH_SOURCE", "admin")
    DB_NAME = "rag_db"
    COLLECTION_NAME = "documents"
    
    EMBEDDINGS_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Configuraciones de cache
    CACHE_ENABLED = env.bool("CACHE_ENABLED", True)
    CACHE_MAX_SIZE = env.int("CACHE_MAX_SIZE", 1000)
    
    # Configuraciones de chunks
    CHUNK_SIZE = env.int("CHUNK_SIZE", 1000)
    CHUNK_OVERLAP = env.int("CHUNK_OVERLAP", 200)
    
    # Configuraciones de API
    MAX_UPLOAD_SIZE = env.int("MAX_UPLOAD_SIZE", 10 * 1024 * 1024)  # 10MB por defecto
    
settings = Settings()