from pydantic import BaseModel, Field, validator
from typing import List, Optional

class ChatMessage(BaseModel):
    """
    Modelo para representar un mensaje en el chat.
    
    Attributes:
        role (str): Rol del mensaje (system, user, assistant)
        content (str): Contenido del mensaje
    """
    role: str
    content: str

    @validator('role')
    def validate_role(cls, v):
        if v not in ['system', 'user', 'assistant']:
            raise ValueError('role must be system, user, or assistant')
        return v

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    """
    Modelo para las solicitudes de chat.
    
    Attributes:
        messages (List[ChatMessage]): Lista de mensajes del chat
        temperature (float): Temperatura para la generación de texto (0-1)
        max_tokens (int): Número máximo de tokens a generar
    """
    messages: List[ChatMessage]
    temperature: float = Field(default=0.5, ge=0.0, le=1.0)
    max_tokens: int = Field(default=1024, gt=0, le=4096)

class ChatResponse(BaseModel):
    """
    Modelo para las respuestas del chat.
    
    Attributes:
        response (str): Texto de respuesta generado
        sources (Optional[List[dict]]): Fuentes utilizadas para generar la respuesta
    """
    response: str
    sources: Optional[List[dict]] = None

class UploadResponse(BaseModel):
    """
    Modelo para las respuestas de subida de archivos.
    
    Attributes:
        message (str): Mensaje de estado de la operación
        document_count (int): Número de documentos procesados
    """
    message: str
    document_count: int
