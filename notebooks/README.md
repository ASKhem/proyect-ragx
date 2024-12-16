# 📓 Implementación Simple de RAG Usando Dos Notebooks

Este directorio contiene dos notebooks de Jupyter que demuestran implementaciones simples de Generación Aumentada por Recuperación (RAG) usando diferentes fuentes de datos.
Se podría considrar una versión simplificado pero efectriva del proyecto general.

## 📚 Descripción de los Notebooks

### 1. context_web_rag.ipynb
- Implementa RAG para recuperación de contenido web
- Características:
  - Web scraping usando BeautifulSoup
  - Segmentación de texto
  - Embeddings vectoriales con sentence-transformers
  - Búsqueda por similitud usando FAISS
  - Integración con la API de NVIDIA para respuestas LLM

### 2. context_pdf_rag.ipynb
- Implementa RAG para recuperación de documentos PDF
- Características:
  - Extracción de texto PDF usando PyPDF
  - Segmentación de texto
  - Embeddings vectoriales con sentence-transformers
  - Búsqueda por similitud usando FAISS
  - Integración con la API de NVIDIA para respuestas LLM

## 🛠️ Componentes Comunes

Ambos notebooks comparten estas funcionalidades principales:
- Segmentación de texto con tamaño configurable
- Creación de almacén vectorial usando FAISS
- Búsqueda semántica basada en similitud de coseno
- Formateo de prompts para LLM
- Respuestas en streaming del LLM

## 🔧 Requisitos

- Python 3.11+
- Dependencias principales:
  - sentence-transformers
  - faiss-cpu
  - beautifulsoup4
  - pypdf
  - requests
  - openai (para integración con API)

## 📝 Uso

1. Instalar las dependencias requeridas si no lo hiciste antes.
2. Configurar las credenciales de la API de NVIDIA
3. Para RAG web: Usar `context_web_rag.ipynb` con tu URL objetivo
4. Para RAG PDF: Usar `context_pdf_rag.ipynb` con tus archivos PDF en el directorio `pdfs/`

Las respuestas se generarán basándose en el contexto recuperado del contenido web o documentos PDF.