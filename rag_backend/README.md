# 🚀 API RAG con NVIDIA LLM

## 📝 Descripción

Esta es una API RAG (Retrieval-Augmented Generation) que utiliza el modelo LLM de NVIDIA para generar respuestas contextuales basadas en documentos. La API permite cargar documentos PDF y realizar consultas sobre ellos utilizando técnicas avanzadas de procesamiento de lenguaje natural.

## ⭐ Características

- 🤖 Integración con NVIDIA LLM (llama-3.1-nemotron-70b-instruct)
- 📄 Procesamiento de documentos PDF
- 🔍 Búsqueda semántica con FAISS
- 💾 Almacenamiento en MongoDB
- 🔄 Sistema de caché para respuestas
- 🚀 API RESTful con FastAPI
- 📦 Embeddings con sentence-transformers

## 🛠️ Tecnologías Utilizadas

- 🐍 Python 3.8+
- ⚡ FastAPI
- 🍃 MongoDB
- 🔍 FAISS para búsqueda vectorial
- 🤖 NVIDIA LLM API
- 🔤 Sentence Transformers
- 📄 PyPDF para procesamiento de documentos

## 📋 Requisitos Previos

- Python 3.8 o superior
- MongoDB
- NVIDIA API Key
- Pip o Conda

## 🔧 Instalación
1. Crear environment
```bash
conda create -n ragx python=3.11 
```

2. Instalar dependencias

```bash
pip install -r requirements.txt
```
Si  te da este error:
```bash
ERROR: ERROR: Failed to build installable wheels for some pyproject.toml based projects (faiss-cpu)
```

Simplemente ejecutar el siguiente comando

```bash
conda install -c pytorch faiss-cpu
```

Tardará alrededor de 4 minutos

3. Crear un archivo `.env` en el directorio raíz y agregar las variables de entorno

```bash
NVIDIA_API_KEY=tu_api_key_nvidia
MONGODB_URL=tu_url_mongodb
MONGODB_USER=tu_usuario
MONGODB_PASSWORD=tu_contraseña
MONGODB_AUTH_SOURCE=admin
CACHE_ENABLED=true
CACHE_MAX_SIZE=1000
```

## 🚀 Ejecutar la Aplicación

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🔌 Endpoints de la API

### 📤 Documentos

- `POST /upload` - Subir documento PDF
  - Acepta archivos PDF
  - Retorna conteo de documentos procesados

### 💬 Chat

- `POST /chat` - Realizar consulta al LLM
  - Acepta mensajes y parámetros de generación
  - Retorna respuesta y fuentes relevantes

### 🏥 Monitoreo

- `GET /health` - Verificar estado del servicio

## ⚠️ Manejo de Errores

La API utiliza códigos de respuesta HTTP estándar:

- ✅ 200: Éxito
- 🆕 201: Creado
- ❌ 400: Solicitud Incorrecta (ej: archivo no válido)
- 💥 500: Error Interno del Servidor

## 🔒 Consideraciones de Seguridad

- Autenticación requerida para NVIDIA API
- Validación de tipos de archivo
- Límite de tamaño en uploads (10MB por defecto)
- Conexión segura a MongoDB

## 🎯 Características Principales

### Sistema RAG

- Procesamiento de documentos en chunks inteligentes
- Embeddings con sentence-transformers
- Búsqueda semántica con FAISS
- Caché de respuestas para consultas frecuentes

### Optimizaciones

- Procesamiento en batch de documentos
- Índices FAISS por archivo
- Conexión pooling con MongoDB
- Workers múltiples para mejor rendimiento

## 📖 Documentación de la API

La documentación interactiva de la API está disponible en:

- Swagger UI: `/docs`
- ReDoc: `/redoc`

## 💾 Configuración de MongoDB

La aplicación es compatible tanto con MongoDB local como con MongoDB Atlas.

### Opción 1: MongoDB Local

```bash
MONGODB_URL=mongodb://localhost:27017
MONGODB_USER=
MONGODB_PASSWORD=
MONGODB_AUTH_SOURCE=admin
```

### Opción 2: MongoDB Atlas

```bash
MONGODB_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority
MONGODB_USER=tu_usuario_atlas
MONGODB_PASSWORD=tu_password_atlas
MONGODB_AUTH_SOURCE=admin
```

> 💡 **Nota**: Si usas MongoDB Atlas, asegúrate de:

> - Configurar las IPs permitidas en la lista blanca de Atlas
> - Usar las credenciales correctas del cluster
> - Tener una conexión estable a internet

## 📁 Estructura del Proyecto

```
.
├── app/
│   ├── __init__.py
│   ├── config.py           # Configuraciones y variables de entorno
│   ├── models.py           # Modelos Pydantic para validación de datos
│   └── services/
│       ├── __init__.py
│       ├── document_service.py    # Gestión de documentos y búsqueda vectorial
│       └── llm_service.py         # Integración con NVIDIA LLM
├── main.py                 # Punto de entrada y rutas de la API
├── requirements.txt        # Dependencias del proyecto
└── .env                    # Variables de entorno (no versionado)
```

### 🔍 Componentes Principales

#### 📄 `main.py`

- Punto de entrada de la aplicación
- Configuración de FastAPI y middleware
- Definición de endpoints
- Gestión de CORS y compresión GZip

#### 📁 `app/config.py`

- Configuraciones centralizadas
- Carga de variables de entorno
- Parámetros del modelo y base de datos
- Configuraciones de caché y chunks

#### 📁 `app/models.py`

- Modelos Pydantic para:
  - Solicitudes de chat
  - Mensajes
  - Respuestas
  - Uploads de documentos

#### 📁 `app/services/`

##### 📄 `document_service.py`

- Procesamiento de documentos PDF
- Gestión de embeddings
- Búsqueda vectorial con FAISS
- Integración con MongoDB
- Chunking inteligente de texto

##### 📄 `llm_service.py`

- Integración con NVIDIA LLM API
- Gestión de contexto y prompts
- Sistema de caché de respuestas
- Manejo de errores de la API

### 🔄 Flujo de Datos

1. **Carga de Documentos**

```
  PDF → DocumentService → Chunks → Embeddings → MongoDB + FAISS
```

2. **Consultas**

```
  Query → Embeddings → FAISS → Contexto Relevante → LLM → Respuesta
```

### 🛠️ Características Técnicas

- **Singleton Pattern** en servicios para gestión eficiente de recursos
- **Batch Processing** para documentos grandes
- **Connection Pooling** en MongoDB
- **Caché LRU** para respuestas frecuentes
- **Chunking Inteligente** respetando estructura del texto
- **Índices FAISS** separados por documento