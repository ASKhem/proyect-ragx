from openai import OpenAI
from app.config import settings
from app.services.document_service import DocumentService
from app.models import ChatMessage
import logging
from typing import Tuple, List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.client = OpenAI(
            base_url=settings.BASE_URL,
            api_key=settings.API_KEY
        )
        self.doc_service = DocumentService()

    async def generate_response(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.5,
        max_tokens: int = 1024
    ) -> Tuple[str, List[Dict[str, Any]]]:
        if not messages:
            raise ValueError("Messages list cannot be empty")
        
        try:
            user_query = messages[-1].content
            relevant_docs = self.doc_service.search_similar(user_query, limit=2)
            
            messages_with_context = [
                {"role": "system", "content": self._build_system_prompt(relevant_docs)},
                *[{"role": msg.role, "content": msg.content} for msg in messages]
            ]

            completion = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=messages_with_context,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )

            response_text = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    response_text += chunk.choices[0].delta.content

            return response_text, relevant_docs

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    @staticmethod
    def _build_system_prompt(docs: List[Dict[str, Any]]) -> str:
        context = "\n\n".join(
            f"De {doc['filename']}:\n{doc['content']}"
            for doc in docs
        )
        
        return (
            "Utiliza el siguiente contexto para responder la pregunta del usuario. "
            "El contexto está organizado por archivos fuente.\n\n"
            f"{context}\n\n"
            "Si la respuesta no se encuentra en el contexto, indícalo."
        )
