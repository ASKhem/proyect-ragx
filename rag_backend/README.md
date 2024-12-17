# 🚀 API RAG con NVIDIA LLM

## 📝 Descripción
Una API de Generación Aumentada por Recuperación (RAG) que utiliza el LLM de NVIDIA para generar respuestas contextuales basadas en documentos. La API permite cargar documentos PDF y realizar consultas utilizando técnicas avanzadas de PLN.

## ⭐ Características Principales
- 🤖 Integración con NVIDIA LLM (llama-3.1-nemotron-70b-instruct)
- 📄 Procesamiento de documentos PDF
- 🔍 Búsqueda semántica con MongoDB Vector Search
- 🚀 API REST con FastAPI
- 📦 Embeddings con sentence-transformers

## 🛠️ Tecnologías
- Python 3.10+
- FastAPI
- MongoDB con Vector Search
- NVIDIA LLM API (vía cliente OpenAI)
- Sentence Transformers
- PyPDF para procesamiento de documentos

## 📋 Requisitos Previos
- Python 3.8 o superior
- MongoDB (con soporte para Vector Search)
- NVIDIA API Key

## 🔧 Instalación

1. Crear y activar el entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Crear archivo `.env` en el directorio raíz:
```bash
NVIDIA_API_KEY=tu_api_key_nvidia
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
MODEL_NAME=nvidia/llama-3.1-nemotron-70b-instruct

MONGODB_URL=tu_url_mongodb
MONGODB_USER=tu_usuario
MONGODB_PASSWORD=tu_contraseña
MONGODB_AUTH_SOURCE=admin

EMBEDDINGS_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

## 🚀 Ejecutar la Aplicación
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🔌 Endpoints de la API

### 📤 Documentos
- `POST /upload` - Subir documento PDF
  - Acepta archivos PDF
  - Retorna número de documentos procesados

### 💬 Chat
- `POST /chat` - Consultar al LLM
  - Acepta mensajes y parámetros de generación
  - Retorna respuesta y fuentes relevantes

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
│       └── llm_service.py         # Integración con NVIDIA LLM
└── main.py                 # Punto de entrada y rutas de la API
```

### 🔍 Componentes Principales

#### 📄 `document_service.py`
- Procesamiento de documentos PDF
- Segmentación de texto
- Generación de embeddings
- Búsqueda semántica con MongoDB

#### 📄 `llm_service.py`
- Integración con NVIDIA LLM API
- Gestión de contexto
- Generación de respuestas

#### 📄 `main.py`
- Aplicación FastAPI
- Endpoints de la API
- Manejo de errores

### 🔄 Flujo de Datos
1. **Carga de Documentos**
```
PDF → Extraer Texto → Crear Segmentos → Generar Embeddings → Almacenar en MongoDB
```

2. **Procesamiento de Consultas**
```
Consulta → Encontrar Documentos Similares → Generar Contexto → Respuesta LLM
```

## ⚠️ Manejo de Errores
- ✅ 200: Éxito
- ❌ 400: Solicitud Incorrecta (ej: archivo inválido)
- 💥 500: Error Interno del Servidor

## 🔒 Consideraciones de Seguridad
- Autenticación requerida para NVIDIA API
- Validación de tipos de archivo
- Conexión segura a MongoDB