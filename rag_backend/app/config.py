from environs import Env

env = Env()
env.read_env()

class Settings:
    def __init__(self):
        # Validar variables críticas
        if not env.str("NVIDIA_API_KEY", ""):
            raise ValueError("NVIDIA_API_KEY is required")
        
        if not env.str("MONGODB_URL", ""):
            raise ValueError("MONGODB_URL is required")
            
        # Inicializar variables
        self.API_KEY = env.str("NVIDIA_API_KEY")
        self.BASE_URL = env.str("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
        self.MODEL_NAME = env.str("MODEL_NAME", "nvidia/llama-3.1-nemotron-70b-instruct")
        
        self.MONGODB_URL = env.str("MONGODB_URL", "mongodb://localhost:27017")
        self.MONGODB_USER = env.str("MONGODB_USER", "")
        self.MONGODB_PASSWORD = env.str("MONGODB_PASSWORD", "")
        self.MONGODB_AUTH_SOURCE = env.str("MONGODB_AUTH_SOURCE", "admin")
        self.MONGODB_MAX_POOL_SIZE = env.int("MONGODB_MAX_POOL_SIZE", 50)
        self.DB_NAME = env.str("DB_NAME", "rag_db")
        self.COLLECTION_NAME = env.str("COLLECTION_NAME", "documents")
        
        self.EMBEDDINGS_MODEL = env.str("EMBEDDINGS_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        self.VECTOR_DIMENSIONS = 384
        
        self.CHUNK_SIZE = env.int("CHUNK_SIZE", 2000)
        self.CHUNK_OVERLAP = env.int("CHUNK_OVERLAP", 400)
        self.MAX_UPLOAD_SIZE = env.int("MAX_UPLOAD_SIZE", 20 * 1024 * 1024)
        
        self.VECTOR_SEARCH_INDEX = env.str("VECTOR_SEARCH_INDEX", "vector_index")
        
        # Configuraciones adicionales para LangChain
        self.RETRIEVER_K = env.int("RETRIEVER_K", 3)
        self.MEMORY_KEY = env.str("MEMORY_KEY", "chat_history")
        
settings = Settings()
