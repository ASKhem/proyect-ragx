# Proyecto RAG-X: Sistema de Recuperación y Generación Aumentada

## 🌟 Visión General

RAG-X es un sistema completo de Recuperación y Generación Aumentada (RAG) que combina una potente API backend con una interfaz de usuario moderna y accesible. El sistema está diseñado para procesar consultas en lenguaje natural y proporcionar respuestas precisas basadas en fuentes de conocimiento específicas.

## 🎯 Demostración

### Interfaz de Usuario

![Interfaz principal](docs/images/img1.png)
*Vista principal de la aplicación*

### Flujo de Trabajo

![Demostración de uso](docs/images/demo.gif)
*Ejemplo de una consulta y respuesta*


## 📓Podemos ver unos ejemplos sencillos en la carpeta notebooks
[Ver ejemplos en notebooks](notebooks/README.md)

##  🤖 MLL usado:
llama-3.1-nemotron-70b-instruct

- NVIDIA proporciona una serie de modelos.
- Nos regala 1000 creditos que sería casi como 5000 respuestas moderadas.

Si quieres buscar otros modelos:
https://build.nvidia.com/nvidia/llama-3_1-nemotron-70b-instruct

### API:

```bash
    from openai import OpenAI

    client = OpenAI(
    base_url = "https://integrate.api.nvidia.com/v1",
    api_key = "$API_KEY_REQUIRED_IF_EXECUTING_OUTSIDE_NGC"
    )

    completion = client.chat.completions.create(
    model="nvidia/llama-3.1-nemotron-70b-instruct",
    messages=[{"role":"user","content":"Write a limerick about the wonders of GPU computing."}],
    temperature=0.5,
    top_p=1,
    max_tokens=1024,
    stream=True
    )

    for chunk in completion:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
```

## 🏗️ Arquitectura del Sistema

El proyecto está dividido en dos componentes principales:

### Frontend (rag_ui/)

- Interfaz de usuario moderna construida con Astro y TypeScript
- Diseño responsive y accesible
- Gestión eficiente de estados y consultas
- [Ver documentación del Frontend](rag_ui/README.md)

### Backend (rag_backend/)

- API RESTful construida con FastAPI
- Procesamiento de lenguaje natural
- Integración con bases de conocimiento
- [Ver documentación del Backend](rag_backend/README.md)

## 🚀 Inicio Rápido

1. Clona el repositorio:

```bash
    git clone https://github.com/ASKhem/proyect-ragx.git
    cd proyect-ragx
```

2. Lee los archivos README.md de cada carpeta para obtener más información sobre cómo configurar y ejecutar el proyecto.


## 📋 Requisitos del Sistema

- Python 3.8+
- Node.js 16+
- npm 7+
- Memoria RAM: 8GB mínimo recomendado
- Espacio en disco: 2GB mínimo

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor, revisa nuestras guías de contribución en [CONTRIBUTING.md](./CONTRIBUTING.md).

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](./LICENSE) para más detalles.

## 📞 Contacto

- Email: khemwirtz@gmail.com
- GitHub Issues: Para reportar problemas o sugerir mejoras
