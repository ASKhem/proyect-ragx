from openai import OpenAI, OpenAIError
from app.config import settings
from app.services.document_service import DocumentService
from app.models import ChatMessage
import logging
from typing import Tuple, List, Dict, Any

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.client = OpenAI(base_url=settings.BASE_URL, api_key=settings.API_KEY)
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
            relevant_docs = self.doc_service.search_similar(messages[-1].content, limit=3)
            
            context = "\n\n".join(
                f"From {doc['filename']} (relevance: {doc['score']}):\n{doc['content']}"
                for doc in relevant_docs
            )
            
            system_message = (
                "You are an expert assistant. Use ONLY the information from the following context to answer. "
                "If the information is not in the context, say so clearly.\n\n"
                f"CONTEXT:\n{context}"
            )
            
            messages_with_context = [
                {"role": "system", "content": system_message},
                *[{"role": msg.role, "content": msg.content} for msg in messages]
            ]

            completion = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=messages_with_context,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )

            response_text = ''.join(
                chunk.choices[0].delta.content
                for chunk in completion
                if chunk.choices[0].delta.content
            )

            return response_text, relevant_docs

        except Exception as e:
            logger.error(f"Response generation error: {str(e)}")
            raise
