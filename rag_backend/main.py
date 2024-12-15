from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.models import ChatRequest, ChatResponse, UploadResponse
from app.services.llm_service import LLMService
from app.services.document_service import DocumentService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG API with NVIDIA LLM")
app.add_middleware(GZipMiddleware, minimum_size=500)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_service = LLMService()
doc_service = DocumentService()

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        logger.info(f"Received chat request with {len(request.messages)} messages")
        response, sources = await llm_service.generate_response(
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        return ChatResponse(response=response, sources=sources)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        doc_count = doc_service.process_pdf(file.file, file.filename)
        return UploadResponse(
            message=f"Successfully processed {file.filename}",
            document_count=doc_count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        workers=4,  # Usar múltiples workers
        reload=False  # Deshabilitar reload en producción
    ) 