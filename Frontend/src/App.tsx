import { Header } from './components/Header'
import { PlayerCard } from './components/PlayerCard'
import { MainPlayerCard } from './components/MainPlayerCard'
import { EventTicker } from './components/EventTicker'
import { TipFeed } from './components/TipFeed'
import { useGameData } from './hooks/useGameData'

export const App = () => {
  const REST_URL = import.meta.env.VITE_REST_URL;
    const WS_URL = import.meta.env.VITE_WS_URL;

  const { metadata, gameState, tips, rawEvents, isConnected, isWaitingForGame } = useGameData(REST_URL, WS_URL);

  return (
      <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col font-sans">

        {/* TOP SECTION */}
        <Header isConnected={isConnected} />

        <main className="px-6 py-6 grow flex flex-col gap-6">

          {/* LOADING SCREEN*/}
          {isWaitingForGame || !gameState || !metadata ? (
              <div className="grow flex items-center justify-center">
                <div className="text-center">
                  <div className="animate-spin w-12 h-12 border-4 border-yellow-500 border-t-transparent rounded-full mx-auto mb-4"></div>
                  <h2 className="text-xl font-bold text-slate-300">Waiting for game to start...</h2>
                  <p className="text-slate-500 text-sm mt-2">Launch League of Legends and enter a match.</p>
                </div>
              </div>
          ) : (

              <>
                {/* PLAYERS SECTION */}
                <section className="grid grid-cols-1 lg:grid-cols-[1fr_auto_1fr] gap-6 items-start">

                  {/* Left column: Allies */}
                  <div className="flex flex-col gap-2">
                    <h2 className="text-sm font-bold text-blue-400 tracking-wider mb-2">ALLIES</h2>
                    <div className="flex flex-col gap-3">
                      {gameState.allies.map((ally, index) => (
                          <PlayerCard key={index} player={ally} patchVersion={metadata.patchVersion} />
                      ))}
                    </div>
                  </div>

                  {/* Middle column: Me */}
                  <div className="flex flex-col gap-2 items-center">
                    <h2 className="text-sm font-bold text-yellow-500 tracking-wider mb-2">ME</h2>
                    <MainPlayerCard player={gameState.me} patchVersion={metadata.patchVersion} />
                  </div>

                  {/* Right column: Enemies */}
                  <div className="flex flex-col gap-2 items-end">
                    <h2 className="text-sm font-bold text-red-400 tracking-wider mb-2">ENEMIES</h2>
                    <div className="flex flex-col gap-3 items-end">
                      {gameState.enemies.map((enemy, index) => (
                          <PlayerCard key={index} player={enemy} patchVersion={metadata.patchVersion} />
                      ))}
                    </div>
                  </div>

                </section>

                {/* TIPS FEED SECTION */}
                <section className="mt-4">
                  <TipFeed tips={tips} />
                </section>

                {/* RAW EVENTS SECTION */}
                <section>
                  <EventTicker events={rawEvents} />
                </section>
              </>
          )}

        </main>
      </div>
  )
}

export default App