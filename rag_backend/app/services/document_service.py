from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from app.config import settings
import uuid
import logging
import numpy as np
from typing import List, Dict, Any
import re
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO

logger = logging.getLogger(__name__)

class DocumentService:
    _instance = None
    _model = None
    _executor = ThreadPoolExecutor(max_workers=4)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DocumentService, cls).__new__(cls)
            cls._model = SentenceTransformer(settings.EMBEDDINGS_MODEL)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.embeddings_model = self._model
            self._init_mongodb()
            self.initialized = True

    def _init_mongodb(self):
        connection_params = {
            'host': settings.MONGODB_URL,
            'w': 1,
            'maxPoolSize': settings.MONGODB_MAX_POOL_SIZE,
            'retryWrites': True,
            'connectTimeoutMS': 5000,
            'serverSelectionTimeoutMS': 5000
        }

        if settings.MONGODB_USER and settings.MONGODB_PASSWORD:
            connection_params.update({
                'username': settings.MONGODB_USER,
                'password': settings.MONGODB_PASSWORD,
                'authSource': settings.MONGODB_AUTH_SOURCE
            })

        self.client = MongoClient(**connection_params)
        self.db = self.client[settings.DB_NAME]
        self.collection = self.db[settings.COLLECTION_NAME]
        logger.info("MongoDB connection initialized")

    def search_similar(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        try:
            query_embedding = self._get_embedding(query)
            
            return list(self.collection.aggregate([
                {
                    "$vectorSearch": {
                        "index": settings.VECTOR_SEARCH_INDEX,
                        "path": "embedding",
                        "queryVector": query_embedding.tolist(),
                        "numCandidates": limit * 10,
                        "limit": limit
                    }
                },
                {
                    "$project": {
                        "content": 1,
                        "filename": 1,
                        "score": {"$meta": "vectorSearchScore"},
                        "_id": 0
                    }
                }
            ]))
            
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []

    @lru_cache(maxsize=settings.CACHE_MAX_SIZE)
    def _get_embedding(self, text: str) -> np.ndarray:
        return self.embeddings_model.encode(text, show_progress_bar=False)

    def _chunk_text(self, text: str) -> List[str]:
        text = re.sub(r'\s+', ' ', text).strip()
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence_size = len(sentence)
            
            if current_size + sentence_size > settings.CHUNK_SIZE and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_size = 0
            
            current_chunk.append(sentence)
            current_size += sentence_size
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
            
        return [chunk for chunk in chunks if len(chunk.strip()) >= 50]

    def process_pdf(self, file, filename: str) -> int:
        try:
            pdf_content = BytesIO(file.read())
            pdf_reader = PdfReader(pdf_content)
            all_text = " ".join(
                page.extract_text() 
                for page in pdf_reader.pages
            )
            
            chunks = self._chunk_text(all_text)
            
            def create_document(chunk: str) -> Dict[str, Any]:
                return {
                    "id": str(uuid.uuid4()),
                    "content": chunk,
                    "embedding": self._get_embedding(chunk).tolist(),
                    "filename": filename
                }
            
            documents = list(self._executor.map(create_document, chunks))
            
            if documents:
                self.collection.insert_many(documents, ordered=False)
            
            return len(documents)
            
        except Exception as e:
            logger.error(f"PDF processing error: {str(e)}")
            raise
