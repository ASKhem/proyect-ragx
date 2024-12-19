from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from app.config import settings
import uuid
import logging
from io import BytesIO
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

class DocumentService:
    """
    Servicio para el procesamiento de documentos y búsqueda semántica.
    
    Este servicio maneja:
    - Procesamiento de archivos PDF
    - Generación de embeddings
    - Búsqueda semántica en MongoDB
    """

    def __init__(self):
        """Inicializa el servicio con el modelo de embeddings y conexión a MongoDB."""
        self.embeddings_model = SentenceTransformer(settings.EMBEDDINGS_MODEL)
        self.client = MongoClient(settings.MONGODB_URL)
        if settings.MONGODB_USER:
            self.client = MongoClient(
                settings.MONGODB_URL,
                username=settings.MONGODB_USER,
                password=settings.MONGODB_PASSWORD,
                authSource=settings.MONGODB_AUTH_SOURCE
            )
        self.collection = self.client[settings.DB_NAME][settings.COLLECTION_NAME]

    async def __aenter__(self):
        """Método para usar el servicio como context manager."""
        return self

    async def __aexit__(self, *args):
        """Limpia recursos al salir del context manager."""
        await self.close()

    async def close(self):
        """Cierra las conexiones del servicio."""
        self.client.close()

    def search_similar(self, query: str, limit: int = 5):
        """
        Busca documentos similares a la consulta proporcionada.

        Args:
            query: Texto de consulta
            limit: Número máximo de resultados a retornar

        Returns:
            Lista de documentos similares con su contenido, nombre y puntuación
        """
        try:
            query_embedding = self.embeddings_model.encode(query)
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
            return [{
                "content": doc.get('content', ''),
                "filename": doc.get('filename', 'Unknown source'),
                "score": round(float(doc.get('score', 0)), 4)
            } for doc in results if doc.get('content')]
        except Exception as e:
            logger.error(f"Vector search error: {str(e)}")
            return []

    def process_pdf(self, file, filename: str):
        """
        Procesa un archivo PDF y almacena su contenido en la base de datos.

        Args:
            file: Objeto de archivo PDF
            filename: Nombre del archivo

        Returns:
            Número de documentos procesados y almacenados

        Raises:
            ValueError: Si el archivo excede el tamaño máximo
            Exception: Para otros errores durante el procesamiento
        """
        try:
            file_content = file.read()
            if len(file_content) > settings.MAX_UPLOAD_SIZE:
                raise ValueError(f"File size exceeds maximum limit of {settings.MAX_UPLOAD_SIZE/1024/1024}MB")
            
            pdf = PdfReader(BytesIO(file_content))
            text = " ".join(page.extract_text() for page in pdf.pages)
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
                length_function=len,
                separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
            )
            
            chunks = text_splitter.split_text(text)
            
            documents = [{
                "id": str(uuid.uuid4()),
                "content": chunk,
                "embedding": self.embeddings_model.encode(chunk).tolist(),
                "filename": filename,
                "chunk_size": len(chunk)
            } for chunk in chunks]
            
            if documents:
                self.collection.insert_many(documents, ordered=False)
            
            logger.info(f"Processed {len(documents)} chunks from {filename}. "
                    f"Average chunk size: {sum(len(d['content']) for d in documents)/len(documents):.0f} chars")
            
            return len(documents)
        except Exception as e:
            logger.error(f"PDF processing error: {str(e)}")
            raise
