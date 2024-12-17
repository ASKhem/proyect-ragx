from environs import Env

env = Env()
env.read_env()

class Settings:
    API_KEY = env.str("NVIDIA_API_KEY")
    BASE_URL = env.str("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
    MODEL_NAME = env.str("MODEL_NAME", "nvidia/llama-3.1-nemotron-70b-instruct")
    
    MONGODB_URL = env.str("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_USER = env.str("MONGODB_USER", "")
    MONGODB_PASSWORD = env.str("MONGODB_PASSWORD", "")
    MONGODB_AUTH_SOURCE = env.str("MONGODB_AUTH_SOURCE", "admin")
    MONGODB_MAX_POOL_SIZE = env.int("MONGODB_MAX_POOL_SIZE", 50)
    DB_NAME = env.str("DB_NAME", "rag_db")
    COLLECTION_NAME = env.str("COLLECTION_NAME", "documents")
    
    EMBEDDINGS_MODEL = env.str("EMBEDDINGS_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    VECTOR_DIMENSIONS = 384
    
    CHUNK_SIZE = env.int("CHUNK_SIZE", 1000)
    CHUNK_OVERLAP = env.int("CHUNK_OVERLAP", 200)
    MAX_UPLOAD_SIZE = env.int("MAX_UPLOAD_SIZE", 20 * 1024 * 1024)
    
    VECTOR_SEARCH_INDEX = env.str("VECTOR_SEARCH_INDEX", "vector_index")
    
settings = Settings()
