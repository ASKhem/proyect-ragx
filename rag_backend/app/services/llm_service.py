from openai import OpenAI
from app.config import settings
from app.services.document_service import DocumentService
import logging
import openai
from functools import lru_cache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.client = OpenAI(
            base_url=settings.BASE_URL,
            api_key=settings.API_KEY
        )
        self.doc_service = DocumentService()
        self.response_cache = {}

    async def _get_cached_response(self, messages, temperature, max_tokens):
        try:
            user_query = messages[-1].content if messages else ""
            if not user_query:
                raise ValueError("No se proporcionó una consulta válida")
            
            relevant_docs = self.doc_service.search_similar(user_query, limit=2)
            
            # Limitar el contexto
            max_context_length = 1000  # Reducir el contexto
            docs_by_file = {}
            current_length = 0
            
            for doc in relevant_docs:
                if current_length >= max_context_length:
                    break
                if doc['filename'] not in docs_by_file:
                    docs_by_file[doc['filename']] = []
                docs_by_file[doc['filename']].append(doc['content'])
                current_length += len(doc['content'])
            
            # Construir el prompt con el contexto organizado
            context_parts = []
            for filename, contents in docs_by_file.items():
                context_parts.append(f"De {filename}:\n" + "\n".join(contents))
            
            context = "\n\n".join(context_parts)
            system_message = (
                "Utiliza el siguiente contexto para responder la pregunta del usuario. "
                "El contexto está organizado por archivos fuente.\n\n"
                f"{context}\n\n"
                "Si la respuesta no se encuentra en el contexto, indícalo."
            )
            
            messages_with_context = [
                {"role": "system", "content": system_message},
                *[{"role": msg.role, "content": msg.content} for msg in messages]
            ]

            logger.info("Sending request to LLM API...")
            try:
                completion = self.client.chat.completions.create(
                    model=settings.MODEL_NAME,
                    messages=messages_with_context,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True
                )

                response_text = ""
                for chunk in completion:
                    if chunk.choices[0].delta.content is not None:
                        response_text += chunk.choices[0].delta.content

                return response_text, relevant_docs
            except openai.AuthenticationError as auth_error:
                logger.error(f"Authentication failed with NVIDIA API: {str(auth_error)}")
                raise Exception("Error de autenticación con la API de NVIDIA. Por favor, verifica tu API key.")
            except openai.APIError as api_error:
                logger.error(f"NVIDIA API error: {str(api_error)}")
                raise Exception("Error al comunicarse con la API de NVIDIA. Por favor, intenta más tarde.")
            
        except Exception as e:
            logger.error(f"Error in _get_cached_response: {str(e)}", exc_info=True)
            raise

    async def generate_response(self, messages, temperature=0.5, max_tokens=200):
        if not messages:
            raise ValueError("Messages list cannot be empty")
        
        query = messages[-1].content
        cache_key = f"{query}_{temperature}_{max_tokens}"
        
        try:
            if cache_key in self.response_cache:
                return self.response_cache[cache_key]
            
            response = await self._get_cached_response(messages, temperature, max_tokens)
            self.response_cache[cache_key] = response
            return response
        except Exception as e:
            logger.error(f"Error in generate_response: {str(e)}", exc_info=True)
            raise