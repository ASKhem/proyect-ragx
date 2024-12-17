import axios from 'axios';
import debounce from 'lodash/debounce';

const API_URL = 'http://localhost:8000';

export interface QueryResponse {
    answer: string;
    sources?: Array<{
        content: string;
        filename: string;
        score: number;
    }>;
}

export interface ChatMessage {
    role: string;
    content: string;
}


export interface UploadResponse {
    message: string;
    document_count: number;
}

export const chatService = {
    sendMessage: debounce(async (messages: ChatMessage[]) => {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept-Encoding': 'gzip'
            },
            body: JSON.stringify({ messages })
        });
        return response.json();
    }, 300)
};

export const ragApi = {
    async query(question: string): Promise<QueryResponse> {
        try {
            const response = await axios.post(`${API_URL}/chat`, { 
                messages: [{ role: "user", content: question }]
            });
            return { 
                answer: response.data.response,
                sources: response.data.sources
            };
        } catch (error) {
            console.error('Error en la consulta RAG:', error);
            throw error;
        }
    },

    async uploadFile(file: File): Promise<UploadResponse> {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post(`${API_URL}/upload`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            return response.data;
        } catch (error) {
            console.error('Error al subir archivo:', error);
            throw error;
        }
    }
};