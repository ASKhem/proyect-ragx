export default function LoadingAnimation() {
    return (
        <div className="flex items-center justify-center px-4">
            <div className="relative inline-flex">
                {/* Círculo exterior rotante */}
                <div className="w-6 h-6 border-2 border-blue-400 border-t-pink-400 rounded-full animate-spin"></div>
                
                {/* Círculo interior pulsante */}
                <div className="absolute top-1/2 left-1/2 w-3 h-3 bg-gradient-to-r from-blue-400 to-pink-400 rounded-full -translate-x-1/2 -translate-y-1/2 animate-pulse"></div>
                
                {/* Solo dos puntos decorativos */}
                <div className="absolute -top-0.5 left-1/2 w-1.5 h-1.5 bg-blue-300 rounded-full animate-ping"></div>
                <div className="absolute -bottom-0.5 left-1/2 w-1.5 h-1.5 bg-pink-300 rounded-full animate-ping [animation-delay:0.3s]"></div>
            </div>
        </div>
    );
} 