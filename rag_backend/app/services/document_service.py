from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from app.config import settings
import uuid
import logging
import numpy as np
import faiss
from collections import defaultdict
from functools import lru_cache
from typing import List, Dict
import re
from itertools import islice

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentService:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DocumentService, cls).__new__(cls)
            # Cargar el modelo una sola vez
            cls._model = SentenceTransformer(settings.EMBEDDINGS_MODEL)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.embeddings_model = self._model
            self.client = None
            self.db = None
            self.collection = None
            self._connect_mongodb()
            self.initialized = True

    def _connect_mongodb(self):
        try:
            if self.client is None:
                connection_params = {
                    'host': settings.MONGODB_URL,
                    'w': 1,
                    'maxPoolSize': 50,
                    'retryWrites': True,
                    'connectTimeoutMS': 5000,
                    'serverSelectionTimeoutMS': 5000
                }

                # Agregar credenciales solo si están configuradas
                if settings.MONGODB_USER and settings.MONGODB_PASSWORD:
                    connection_params.update({
                        'username': settings.MONGODB_USER,
                        'password': settings.MONGODB_PASSWORD,
                        'authSource': settings.MONGODB_AUTH_SOURCE
                    })

                self.client = MongoClient(**connection_params)
                
                # Verificar conexión
                try:
                    self.client.admin.command('ping')
                    logger.info("Successfully connected to MongoDB")
                except Exception as ping_error:
                    logger.error(f"Failed to ping MongoDB: {str(ping_error)}")
                    if "bad auth" in str(ping_error).lower():
                        raise Exception(
                            "Authentication failed. Please check your MongoDB credentials "
                            "(MONGODB_USER, MONGODB_PASSWORD, and MONGODB_AUTH_SOURCE)"
                        )
                    raise
                
                self.db = self.client[settings.DB_NAME]
                self.collection = self.db[settings.COLLECTION_NAME]
                
                # Crear índices si no existen
                try:
                    self.collection.create_index(
                        [("filename", 1), ("embedding", 1)],
                        background=True
                    )
                except Exception as index_error:
                    logger.warning(f"Failed to create index: {str(index_error)}")
                
                self.indices = defaultdict(self._create_index)
                self._load_existing_vectors()
                
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {str(e)}")
            if hasattr(self, 'client') and self.client:
                self.client.close()
                self.client = None
            raise Exception(f"MongoDB connection error: {str(e)}")

    def __del__(self):
        try:
            if hasattr(self, 'client') and self.client:
                self.client.close()
                logger.info("MongoDB connection closed")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {str(e)}")

    def _create_index(self):
        dimension = 384
        # Usar IndexFlatIP para conjuntos pequeños
        return faiss.IndexFlatIP(dimension)

    def _load_existing_vectors(self):
        """Carga los vectores existentes en índices FAISS separados por archivo"""
        try:
            # Agrupar documentos por filename
            documents_by_file = defaultdict(list)
            for doc in self.collection.find({}):
                documents_by_file[doc['filename']].append(doc)
            
            # Crear índice para cada archivo
            for filename, docs in documents_by_file.items():
                vectors = np.array([doc['embedding'] for doc in docs], dtype='float32')
                self.indices[filename].add(vectors)
                logger.info(f"Loaded {len(docs)} vectors for file {filename}")
        except Exception as e:
            logger.warning(f"Could not load existing vectors: {str(e)}")

    @lru_cache(maxsize=1000)
    def _get_embedding(self, text):
        """Cache los embeddings para textos frecuentes"""
        return self.embeddings_model.encode(text)

    def search_similar(self, query, limit=5):
        try:
            # Usar cache para query embeddings
            query_embedding = self._get_embedding(query)
            query_vector = np.array([query_embedding], dtype='float32')
            
            all_results = []
            
            # Buscar en cada índice
            for filename, index in self.indices.items():
                if index.ntotal > 0:  # Si el índice tiene vectores
                    scores, indices = index.search(query_vector, min(limit, index.ntotal))
                    
                    # Obtener documentos correspondientes de MongoDB
                    docs = list(self.collection.find({"filename": filename}))
                    
                    for idx, score in zip(indices[0], scores[0]):
                        if idx < len(docs):  # Verificar que el índice es válido
                            doc = docs[idx]
                            all_results.append({
                                'content': doc['content'],
                                'filename': filename,
                                'score': float(score)
                            })
            
            # Ordenar todos los resultados por score y tomar los top k
            all_results.sort(key=lambda x: x['score'], reverse=True)
            return all_results[:limit]
            
        except Exception as e:
            logger.error(f"Error in search_similar: {str(e)}")
            return []

    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Divide el texto en chunks más inteligentes respetando párrafos y oraciones"""
        # Eliminar espacios múltiples y saltos de línea
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Dividir en oraciones (manera simple)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence_size = len(sentence)
            
            if current_size + sentence_size > chunk_size and current_chunk:
                # Guardar el chunk actual
                chunks.append(' '.join(current_chunk))
                # Mantener algunas oraciones para overlap
                overlap_sentences = current_chunk[-2:] if len(current_chunk) > 2 else current_chunk
                current_chunk = overlap_sentences
                current_size = sum(len(s) for s in current_chunk)
            
            current_chunk.append(sentence)
            current_size += sentence_size
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
            
        return chunks

    def _batch_generator(self, items: List, batch_size: int):
        """Genera batches de items para procesamiento eficiente"""
        iterator = iter(items)
        while batch := list(islice(iterator, batch_size)):
            yield batch

    def process_pdf(self, file, filename: str) -> int:
        try:
            pdf_reader = PdfReader(file)
            all_text = ""
            
            # Extraer texto de manera más eficiente
            for page in pdf_reader.pages:
                all_text += page.extract_text() + " "
            
            # Crear chunks más inteligentes
            chunks = self._chunk_text(all_text)
            total_documents = 0
            
            # Procesar en batches para mejor rendimiento y memoria
            for batch in self._batch_generator(chunks, batch_size=32):
                # Filtrar chunks vacíos
                valid_chunks = [chunk for chunk in batch if len(chunk.strip()) > 50]
                
                if not valid_chunks:
                    continue
                
                # Generar embeddings en batch
                embeddings = self.embeddings_model.encode(
                    valid_chunks,
                    batch_size=len(valid_chunks),
                    show_progress_bar=False
                )
                
                # Preparar documentos para inserción
                documents = [
                    {
                        "id": str(uuid.uuid4()),
                        "content": chunk,
                        "embedding": embedding.tolist(),
                        "filename": filename
                    }
                    for chunk, embedding in zip(valid_chunks, embeddings)
                ]
                
                if documents:
                    # Insertar documentos en batch
                    self.collection.insert_many(documents, ordered=False)
                    
                    # Actualizar índice FAISS
                    vectors_array = np.array([doc['embedding'] for doc in documents], dtype='float32')
                    self.indices[filename].add(vectors_array)
                    
                    total_documents += len(documents)
                    
            logger.info(f"Processed {total_documents} chunks for file {filename}")
            return total_documents
            
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise Exception(f"Error processing PDF: {str(e)}") 