from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from app.config import settings
import uuid
import logging
import numpy as np
from typing import List, Dict, Any
import re
from io import BytesIO

logger = logging.getLogger(__name__)

class DocumentService:
    def __init__(self):
        self.embeddings_model = SentenceTransformer(settings.EMBEDDINGS_MODEL)
        self.client = MongoClient(
            settings.MONGODB_URL,
            username=settings.MONGODB_USER or None,
            password=settings.MONGODB_PASSWORD or None,
            authSource=settings.MONGODB_AUTH_SOURCE if settings.MONGODB_USER else None
        )
        self.collection = self.client[settings.DB_NAME][settings.COLLECTION_NAME]

    def search_similar(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        try:
            query_embedding = self.embeddings_model.encode(query, show_progress_bar=False)
            results = self.collection.aggregate([
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
            ])
            return [
                {
                    "content": doc.get('content', ''),
                    "filename": doc.get('filename', 'Unknown source'),
                    "score": round(float(doc.get('score', 0)), 4)
                }
                for doc in results
                if doc.get('content')
            ]
        except Exception as e:
            logger.error(f"Vector search error: {str(e)}", exc_info=True)
            return []

    def process_pdf(self, file, filename: str) -> int:
        try:
            pdf_content = BytesIO(file.read())
            pdf_reader = PdfReader(pdf_content)
            text = " ".join(page.extract_text() for page in pdf_reader.pages)
            
            chunks = [chunk for chunk in re.split(r'(?<=[.!?])\s+', text.strip())
                    if len(chunk.strip()) >= 50]
            
            documents = []
            for chunk in chunks:
                embedding = self.embeddings_model.encode(chunk, show_progress_bar=False)
                documents.append({
                    "id": str(uuid.uuid4()),
                    "content": chunk,
                    "embedding": embedding.tolist(),
                    "filename": filename
                })
            
            if documents:
                self.collection.insert_many(documents, ordered=False)
            
            return len(documents)
        except Exception as e:
            logger.error(f"PDF processing error: {str(e)}")
            raise
