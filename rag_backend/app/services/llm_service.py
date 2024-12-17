from openai import OpenAI
from app.config import settings
from app.models import ChatMessage
import logging
from typing import Tuple, List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from pymongo import MongoClient

logger = logging.getLogger(__name__)

class LLMService:
    """
    Servicio para la interacción con modelos de lenguaje y RAG.
    
    Este servicio maneja:
    - Integración con modelos de chat
    - Generación de respuestas con contexto
    - Búsqueda vectorial en MongoDB
    """

    def __init__(self):
        """Inicializa el servicio con el modelo de chat, embeddings y conexión a MongoDB."""
        self.chat_model = ChatOpenAI(
            base_url=settings.BASE_URL,
            api_key=settings.API_KEY,
            model_name=settings.MODEL_NAME,
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()]
        )
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDINGS_MODEL
        )
        
        self.client = MongoClient(settings.MONGODB_URL)
        if settings.MONGODB_USER:
            self.client = MongoClient(
                settings.MONGODB_URL,
                username=settings.MONGODB_USER,
                password=settings.MONGODB_PASSWORD,
                authSource=settings.MONGODB_AUTH_SOURCE
            )
        
        self.collection = self.client[settings.DB_NAME][settings.COLLECTION_NAME]
        self.vector_store = MongoDBAtlasVectorSearch(
            embedding=self.embeddings,
            collection=self.collection,
            index_name=settings.VECTOR_SEARCH_INDEX,
            text_key="content",
            embedding_key="embedding"
        )
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )

    async def __aenter__(self):
        """Método para usar el servicio como context manager."""
        return self

    async def __aexit__(self, *args):
        """Limpia recursos al salir del context manager."""
        await self.close()

    async def close(self):
        """Cierra las conexiones del servicio."""
        self.client.close()

    async def generate_response(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.5,
        max_tokens: int = 1024
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Genera una respuesta usando el modelo de lenguaje y RAG.

        Args:
            messages: Lista de mensajes del chat
            temperature: Control de aleatoriedad en la generación (0-1)
            max_tokens: Longitud máxima de la respuesta

        Returns:
            Tuple con la respuesta generada y lista de fuentes utilizadas

        Raises:
            ValueError: Si no se recibe una respuesta válida del modelo
            Exception: Para otros errores durante la generación
        """
        try:
            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.chat_model,
                retriever=self.vector_store.as_retriever(
                    search_kwargs={"k": settings.RETRIEVER_K}
                ),
                memory=self.memory,
                return_source_documents=True,
                verbose=True,
                chain_type="stuff",
                output_key="answer"
            )
            
            result = await qa_chain.ainvoke({
                "question": messages[-1].content,
                "chat_history": [(msg.role, msg.content) for msg in messages[:-1]]
            })
            
            self.memory.clear()
            
            sources = [{
                "content": doc.page_content,
                "filename": doc.metadata.get("filename", "Unknown source"),
                "score": doc.metadata.get("score", 0)
            } for doc in result.get("source_documents", [])]
            
            if "answer" not in result:
                raise ValueError("No se recibió una respuesta válida del modelo")
                
            return result["answer"], sources

        except Exception as e:
            logger.error(f"Response generation error: {str(e)}", exc_info=True)
            raise
