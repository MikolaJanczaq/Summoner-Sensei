interface HeaderProps {
    isConnected?: boolean;
}

export const Header = ({ isConnected = true }: HeaderProps) => {
    return (

        <header className="flex justify-between items-center px-6 py-4 bg-slate-900 border-b border-slate-800">

            {/* APP TITLE */}
            <h1 className="text-xl font-black text-yellow-500 tracking-widest uppercase">
                LoL Assistant
            </h1>

            {/* STATUS LIGHT */}
            <div className="flex items-center gap-3 bg-slate-950 px-4 py-2 rounded-full border border-slate-800 shadow-inner">

                <div className="relative flex items-center justify-center">
                    <div className={`absolute w-4 h-4 rounded-full opacity-50 blur-sm ${
                        isConnected ? 'bg-emerald-500' : 'bg-red-600'
                    }`}></div>
                    <div className={`relative w-2.5 h-2.5 rounded-full ${
                        isConnected ? 'bg-emerald-400' : 'bg-red-500'
                    }`}></div>
                </div>

                {/* status text */}
                <span className={`text-xs font-bold tracking-wide uppercase ${
                    isConnected ? 'text-emerald-500' : 'text-red-500'
                }`}>
          {isConnected ? 'Connected to client' : 'Disconnected'}
        </span>

            </div>

        </header>
    )
}