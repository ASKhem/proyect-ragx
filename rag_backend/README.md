# 🚀 API RAG con NVIDIA LLM

## 📝 Descripción
Una API de Generación Aumentada por Recuperación (RAG) que utiliza el LLM de NVIDIA para generar respuestas contextuales basadas en documentos. La API permite cargar documentos PDF y realizar consultas utilizando técnicas avanzadas de PLN.

## ⭐ Características Principales
- 🤖 Integración con NVIDIA LLM (llama-3.1-nemotron-70b-instruct)
- 📄 Procesamiento de documentos PDF
- 🔍 Búsqueda semántica con MongoDB Vector Search
- 🚀 API REST con FastAPI
- 📦 Embeddings con sentence-transformers
- 🧠 Memoria de conversación con LangChain
- 🔄 Streaming de respuestas
- ⚡ Procesamiento asíncrono

## 🛠️ Tecnologías
- Python 3.10+
- FastAPI
- MongoDB con Vector Search
- NVIDIA LLM API (vía cliente OpenAI)
- Sentence Transformers
- LangChain
- PyPDF2 para procesamiento de documentos

## 📋 Requisitos Previos
- Python 3.8 o superior
- MongoDB (con soporte para Vector Search)
- NVIDIA API Key

## 🔧 Instalación

1. Crear y activar el entorno virtual e Instalar dependencias:
```bash
conda env create -f environment.yml
```

2. Crear archivo `.env` en el directorio raíz:
```bash
NVIDIA_API_KEY=tu_api_key_nvidia
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
MODEL_NAME=nvidia/llama-3.1-nemotron-70b-instruct

MONGODB_URL=tu_url_mongodb
MONGODB_USER=tu_usuario
MONGODB_PASSWORD=tu_contraseña
MONGODB_AUTH_SOURCE=admin
DB_NAME=rag_db
COLLECTION_NAME=documents

EMBEDDINGS_MODEL=sentence-transformers/all-MiniLM-L6-v2
VECTOR_SEARCH_INDEX=vector_index
RETRIEVER_K=3

# Configuraciones opcionales
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_UPLOAD_SIZE=20971520  # 20MB en bytes
MONGODB_MAX_POOL_SIZE=50
```

## 🚀 Ejecutar la Aplicación
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🔌 Endpoints de la API

### 📤 Documentos
- `POST /upload` - Subir documento PDF
  - Acepta archivos PDF (máx. 20MB)
  - Retorna número de documentos procesados
  - Segmenta automáticamente el texto
  - Genera embeddings para búsqueda semántica

### 💬 Chat
- `POST /chat` - Consultar al LLM
  - Parámetros:
    - messages: Lista de mensajes del chat
    - temperature: Control de creatividad (0-1)
    - max_tokens: Longitud máxima de respuesta
  - Retorna:
    - response: Respuesta generada
    - sources: Fuentes relevantes utilizadas

### 🏥 Monitoreo
- `GET /health` - Verificar estado del servicio

## 📁 Estructura del Proyecto
```
.
├── app/
│   ├── config.py           # Configuración y variables de entorno
│   ├── models.py           # Modelos Pydantic
│   └── services/
│       ├── document_service.py    # Procesamiento de documentos y búsqueda vectorial
│       └── llm_service.py         # Integración con NVIDIA LLM y LangChain
└── main.py                 # Punto de entrada y rutas de la API
```

### 🔍 Componentes Principales

#### 📄 `document_service.py`
- Procesamiento de documentos PDF
- Segmentación de texto
- Generación de embeddings
- Búsqueda semántica con MongoDB Vector Search
- Manejo asíncrono de recursos

#### 📄 `llm_service.py`
- Integración con NVIDIA LLM API
- Gestión de contexto con LangChain
- Memoria de conversación
- Streaming de respuestas
- Recuperación de documentos relevantes

#### 📄 `models.py`
- Validación de datos con Pydantic
- Modelos para mensajes de chat
- Modelos para respuestas y subida de archivos

### 🔄 Flujo de Datos
1. **Carga de Documentos**
```
PDF → Extraer Texto → Segmentar → Generar Embeddings → MongoDB Vector Store
```

2. **Procesamiento de Consultas**
```
Query → Vector Search → LangChain RAG → Streaming LLM Response
```

## ⚠️ Manejo de Errores
- ✅ 200: Éxito
- ❌ 400: Solicitud Incorrecta
  - Archivo no es PDF
  - Tamaño excede límite
  - Parámetros inválidos
- 💥 500: Error Interno
  - Error de conexión a MongoDB
  - Error en procesamiento de PDF
  - Error en generación LLM

## 🔒 Consideraciones de Seguridad
- Autenticación requerida para NVIDIA API
- Validación de tipos de archivo
- Límite de tamaño de archivo
- Conexión segura a MongoDB
- Manejo seguro de credenciales con variables de entorno

## 🔍 Monitoreo y Logging
- Logging estructurado
- Trazabilidad de errores
- Métricas de procesamiento