# 🎨 Interfaz RAG con Astro & React

## 📝 Descripción

Una interfaz de usuario moderna y responsiva para interactuar con APIs RAG (Retrieval-Augmented Generation). Construida con Astro y React, esta interfaz proporciona una experiencia de chat fluida con soporte para carga de documentos y respuestas contextuales.

## ⭐ Características

- 💬 Interfaz de chat interactiva
- 📄 Soporte para carga de documentos PDF
- ⚡ Streaming de respuestas en tiempo real
- 🎨 Diseño moderno y responsivo
- 🌙 Soporte para modo oscuro
- 🔄 Efectos de animación de escritura
- 📱 Diseño adaptable a móviles

## 🛠️ Tecnologías Utilizadas

- 🚀 Astro 5.0
- ⚛️ React 19
- 🎨 TailwindCSS
- 🔤 TypeScript
- 📝 React Markdown
- ✨ Resaltado de sintaxis
- 🎯 Axios para llamadas API

## 📋 Requisitos Previos

- Node.js 18.17.1 o superior
- npm o yarn
- API RAG ejecutándose en el puerto 8000

## 🔧 Instalación

Instalar dependencias

```bash
npm install
```

## 🚀 Ejecutar la Aplicación

Iniciar el servidor de desarrollo

```bash
    npm run dev
```

Modo Producción

```bash
    npm run build
    npm run start
```

3. Navegar a `http://localhost:3000` en tu navegador


## 🎯 Componentes Principales

### 📱 Componentes de Interfaz

- `Header.tsx` - Navegación y marca
- `QueryForm.tsx` - Interfaz principal de chat
- `MessageList.tsx` - Visualización de mensajes
- `InputForm.tsx` - Entrada de mensajes y carga de archivos
- `LoadingAnimation.tsx` - Estados de carga

## 📁 Estructura del Proyecto

.
├── src/
│ ├── components/ # Componentes React
│ ├── layouts/ # Layouts de Astro
│ ├── pages/ # Páginas de Astro
│ ├── lib/ # Utilidades y API
│ ├── types/ # Tipos TypeScript
│ └── styles/ # Estilos globales
├── public/ # Activos estáticos
├── astro.config.mjs # Configuración de Astro
└── tailwind.config.cjs # Configuración de Tailwind

## 🎨 Estilos

### Características de TailwindCSS

- Animaciones personalizadas
- Efectos de gradiente
- Diseño responsivo
- Soporte para modo oscuro

### Animaciones Personalizadas

- Efecto de escritura de mensajes
- Animaciones de carga
- Transiciones suaves
- Animaciones de gradiente

## 🔌 Integración con API

### Endpoints Utilizados

- `POST /chat` - Enviar mensajes
- `POST /upload` - Subir documentos

### Formato de Mensajes


```typescript
    interface Message {
        role: string;
        content: string;
        isTyping?: boolean;
        isLoading?: boolean;
    }
```

## ⚙️ Archivos de Configuración

### Configuración de Astro

- `astro.config.mjs` - Configuración principal de Astro
- `tailwind.config.cjs` - Configuración de TailwindCSS

## 🔒 Consideraciones de Seguridad

- Sanitización de entradas
- Validación de tipos de archivo
- Límites de tamaño en cargas
- Manejo de errores de API

## 🎯 Características Principales

### Interfaz de Chat

- Actualizaciones en tiempo real
- Soporte para Markdown
- Resaltado de sintaxis de código
- Soporte para adjuntos

### Optimizaciones

- Llamadas API con debounce
- Carga perezosa de componentes
- Re-renderizados eficientes
- Animaciones fluidas

## 📱 Diseño Responsivo

- Enfoque mobile-first
- Layouts flexibles
- Componentes adaptativos
- Interfaz táctil amigable