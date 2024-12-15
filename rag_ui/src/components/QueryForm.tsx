import { useState } from 'react';
import { ragApi } from '../lib/api';
import MessageList from './MessageList';
import InputForm from './InputForm';
import type { Message } from '../types/chat';

export default function QueryForm() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [uploading, setUploading] = useState(false);

    const simulateTyping = (fullMessage: string, messageIndex: number) => {
        let currentText = '';
        const textArray = fullMessage.split('');
        const charsPerTick = 3;
        
        const typeInterval = setInterval(() => {
            if (textArray.length > 0) {
                for (let i = 0; i < charsPerTick && textArray.length > 0; i++) {
                    currentText += textArray.shift();
                }
                
                setMessages(prevMessages =>
                    prevMessages.map((msg, idx) =>
                        idx === messageIndex
                            ? { ...msg, content: currentText, isTyping: true }
                            : msg
                    )
                );
            } else {
                clearInterval(typeInterval);
                setMessages(prevMessages =>
                    prevMessages.map((msg, idx) =>
                        idx === messageIndex
                            ? { ...msg, isTyping: false }
                            : msg
                    )
                );
            }
        }, 10);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = { role: 'user', content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setLoading(true);

        try {
            setMessages(prev => [...prev, { 
                role: 'assistant', 
                content: '', 
                isLoading: true 
            }]);

            const response = await ragApi.query(input);
            
            setMessages(prev => [
                ...prev.slice(0, -1),
                { role: 'assistant', content: '', isTyping: true }
            ]);
            
            simulateTyping(response.answer, messages.length + 1);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleFileUpload = async (file: File) => {
        setUploading(true);
        try {
            const result = await ragApi.uploadFile(file);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: `✅ Archivo procesado: ${file.name}\nSe extrajeron ${result.document_count} fragmentos de texto.`
            }]);
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: '❌ Error al procesar el archivo.'
            }]);
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="max-w-7xl mx-auto h-[86vh] flex flex-col w-full items-center">
            <MessageList messages={messages} />
            
            <div className="pt-6 w-full space-y-4 flex justify-center">
                <InputForm
                    input={input}
                    loading={loading}
                    onInputChange={(e) => setInput(e.target.value)}
                    onSubmit={handleSubmit}
                    onFileUpload={handleFileUpload}
                />
            </div>
        </div>
    );
}