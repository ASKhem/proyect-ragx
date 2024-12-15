import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/cjs/styles/prism';
import LoadingAnimation from './LoadingAnimation';
import { UserCircleIcon } from '@heroicons/react/24/outline';
import type { Message } from '../types/chat';
import { useEffect, useRef } from 'react';

interface MessageListProps {
    messages: Message[];
}

export default function MessageList({ messages }: MessageListProps) {
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]); // Se ejecutará cada vez que messages cambie

    if (messages.length === 0) {
        return (
            <div className="flex-1 p-4 flex items-center justify-center">
                <div className="text-center bg-gray-100 dark:bg-gray-900/80 w-full rounded-2xl px-64 py-40">
                    <h1 className="text-6xl font-extrabold bg-clip-text text-transparent
                        bg-gradient-to-r from-blue-300 to-purple-300 animate-gradient-x">
                        ASKLM Chat
                    </h1>
                    <p className="mt-4 text-gray-600 dark:text-gray-300">
                        La forma más fácil de interactuar con tu información.
                        <br />
                        Soporta archivos PDF y en el futuro TXT, DOCX, y más.
                    </p>
                    <p className="mt-4 text-gray-600 dark:text-gray-400 animate-pulse">
                        Inicia una conversación para comenzar...
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div className="flex-1 overflow-y-auto p-4 space-y-6 ">
            {messages.map((message, index) => (
                <div key={index}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}
                            animate-fadeIn`}>
                    <div className={`flex items-start gap-3 max-w-[85%] sm:max-w-[75%]
                                ${message.role === 'user' ? 'flex-row-reverse' : ''}`}>
                        <div className={`w-10 h-10 rounded-full flex items-center justify-center
                                    ${message.role === 'user'
                                ? 'bg-gradient-to-br from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700'
                                : 'bg-gradient-to-br from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700'}
                                    shadow-lg transform transition-all duration-300 ease-in-out
                                    hover:scale-110 hover:shadow-xl hover:rotate-3
                                    active:scale-95 cursor-pointer
                                    aspect-square`}>
                            {message.role === 'user' ? (
                                <UserCircleIcon className="w-7 h-7 text-white transition-transform duration-300 ease-in-out hover:rotate-12" />
                            ) : (
                                <img
                                    src="/images/nvidia.png"
                                    alt="Nvidia Assistant"
                                    className="w-full h-full rounded-full transition-transform duration-300 ease-in-out hover:rotate-12 object-cover"
                                />
                            )}
                        </div>
                        <div className={`p-4 rounded-2xl shadow-sm
                            ${message.role === 'user'
                                ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-br-none'
                                : 'bg-white dark:bg-gray-800 rounded-bl-none dark:text-gray-100 border border-gray-100 dark:border-gray-700'}
                            transition-all duration-200 hover:shadow-md`}>
                            {message.isLoading ? (
                                <LoadingAnimation />
                            ) : (
                                <div className={`prose prose-sm max-w-none
                                    ${message.role === 'user'
                                        ? 'prose-invert'
                                        : 'dark:prose-invert prose-blue'}`}>
                                    <ReactMarkdown
                                        components={{
                                            code({ node, inline, className, children, ...props }) {
                                                const match = /language-(\w+)/.exec(className || '');
                                                return !inline && match ? (
                                                    <SyntaxHighlighter
                                                        style={vscDarkPlus}
                                                        language={match[1]}
                                                        PreTag="div"
                                                        className="rounded-lg !my-4 !bg-gray-800/50 !p-4 backdrop-blur border border-gray-700/50"
                                                        customStyle={{
                                                            fontSize: '0.95rem',
                                                            lineHeight: '1.5',
                                                            margin: 0,
                                                        }}
                                                        showLineNumbers={true}
                                                        wrapLines={true}
                                                        {...props}
                                                    >
                                                        {String(children).replace(/\n$/, '')}
                                                    </SyntaxHighlighter>
                                                ) : (
                                                    <code className={className} {...props}>
                                                        {children}
                                                    </code>
                                                );
                                            }
                                        }}
                                    >
                                        {message.content}
                                    </ReactMarkdown>
                                </div>
                            )}
                            {message.isTyping && (
                                <div className="flex gap-1 mt-2">
                                    <div className="w-2 h-2 rounded-full bg-current opacity-60 animate-bounce" />
                                    <div className="w-2 h-2 rounded-full bg-current opacity-60 animate-bounce delay-75" />
                                    <div className="w-2 h-2 rounded-full bg-current opacity-60 animate-bounce delay-150" />
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            ))}
            <div ref={messagesEndRef} />
        </div>
    );
}