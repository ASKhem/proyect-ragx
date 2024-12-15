import { BeakerIcon } from '@heroicons/react/24/outline';

export default function Header() {
    return (
        <header className="sticky top-0 z-50 backdrop-blur-xl bg-white dark:bg-gray-800 border-b border-gray-200/50 dark:border-gray-800/50 shadow-sm">
            <div className="mx-auto px-4 py-3 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between">
                    <div className="flex flex-col">
                        <h1 className="text-3xl font-black tracking-tight relative group">
                            <span className="bg-gradient-to-r from-blue-600 to-purple-600
                                bg-clip-text text-transparent animate-gradient-x">
                                ASKLM
                            </span>
                            <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r
                                from-blue-600 to-purple-600 transition-all duration-300
                                group-hover:w-full"></span>
                        </h1>
                        <span className="text-xs text-gray-500 dark:text-gray-400">
                            Powered by Nemotron
                        </span>
                    </div>
                    
                    <nav className="flex items-center space-x-2">
                        <a href="https://github.com/tu-usuario/tu-repo"
                            target="_blank"
                            className="ml-2 p-2 rounded-xl bg-gradient-to-r from-blue-600 to-purple-600
                                text-white shadow-lg shadow-blue-500/20
                                hover:shadow-blue-500/40 hover:scale-105 active:scale-95
                                transition-all duration-200 flex items-center gap-2">
                            <BeakerIcon className="h-5 w-5" />
                            <span className="hidden sm:inline font-medium">Lab</span>
                        </a>
                    </nav>
                </div>
            </div>
        </header>
    );
} 