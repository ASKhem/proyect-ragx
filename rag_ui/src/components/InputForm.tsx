import React from 'react';
import { PaperClipIcon, PaperAirplaneIcon } from '@heroicons/react/24/outline';

interface InputFormProps {
    input: string;
    loading: boolean;
    onInputChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onSubmit: (e: React.FormEvent) => void;
    onFileUpload?: (file: File) => void;
}

export default function InputForm({
    input,
    loading,
    onInputChange,
    onSubmit,
    onFileUpload
}: InputFormProps) {
    const fileInputRef = React.useRef<HTMLInputElement>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file && onFileUpload) {
            onFileUpload(file);
        }
    };

    return (
        <form onSubmit={onSubmit} className="relative flex gap-2 items-center bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-2 w-1/2 min-w-[300px]">
            <div className="flex-1 relative flex items-center">
                <input
                    type="text"
                    value={input}
                    onChange={onInputChange}
                    className="w-full p-4 h-10 bg-transparent rounded-xl focus:outline-none
                            dark:text-white placeholder:text-gray-400 dark:placeholder:text-gray-500"
                    placeholder="Escribe tu mensaje..."
                    disabled={loading}
                />
                <button
                    type="button"
                    onClick={() => fileInputRef.current?.click()}
                    className="absolute right-3 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700
                            text-gray-400 hover:text-gray-600 dark:hover:text-gray-300
                            transition-all duration-200"
                    disabled={loading}
                >
                    <PaperClipIcon className="h-5 w-5" />
                </button>
                <input
                    ref={fileInputRef}
                    type="file"
                    onChange={handleFileChange}
                    className="hidden"
                    accept=".pdf,.doc,.docx,.txt"
                />
            </div>
            <button
                type="submit"
                disabled={loading}
                className="p-3 rounded-xl bg-gradient-to-r from-purple-600 to-blue-600
                        disabled:opacity-50 disabled:cursor-not-allowed
                        transition-all duration-200 hover:scale-105
                        flex items-center justify-center min-w-[48px]"
                aria-label={loading ? 'Enviando...' : 'Enviar mensaje'}
            >
                {loading ? (
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                    <PaperAirplaneIcon className="h-5 w-5" />
                )}
            </button>
        </form>
    );
} 