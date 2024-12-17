from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.models import ChatRequest, ChatResponse, UploadResponse
from app.services.llm_service import LLMService
from app.services.document_service import DocumentService
import logging

logger = logging.getLogger(__name__)
app = FastAPI(title="RAG API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_service = LLMService()
doc_service = DocumentService()

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response, sources = await llm_service.generate_response(
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        return ChatResponse(response=response, sources=sources)
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        doc_count = doc_service.process_pdf(file.file, file.filename)
        return UploadResponse(
            message=f"File {file.filename} processed successfully",
            document_count=doc_count
        )
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 