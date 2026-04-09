import { Header } from './components/Header'
import { PlayerCard } from './components/PlayerCard'
import { MainPlayerCard } from './components/MainPlayerCard'
import { EventTicker } from './components/EventTicker'
import type {Player} from "./types.ts";
import {TipFeed} from "./components/TipFeed.tsx";


const mockAlly: Player = {
  championName: "Jinx",
  level: 14,
  kda: { kills: 4, deaths: 2, assists: 3 },
  items: ["Infinity Edge", "Rapid Firecannon", "Bloodthirster", "Lord Dominik's", "Guardian Angel", ""]
}

export const App = () => {
  return (
      <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col font-sans">

        {/* TOP SECTION */}
        <Header />

        <main className="px-6 py-6 flex-grow flex flex-col gap-6">

          {/* PLAYERS SECTION */}
          <section className="grid grid-cols-1 lg:grid-cols-[1fr_auto_1fr] gap-6 items-start">

            {/* Left column: Allies */}
            <div className="flex flex-col gap-2">
              <h2 className="text-sm font-bold text-blue-400 tracking-wider mb-2">ALLIES</h2>
              <div className="flex flex-col gap-3">
                <PlayerCard player={mockAlly}/>
                <PlayerCard player={mockAlly}/>
                <PlayerCard player={mockAlly}/>
                <PlayerCard player={mockAlly}/>
              </div>
            </div>

            {/* Middle column: Me */}
            <div className="flex flex-col gap-2 items-center">
              <h2 className="text-sm font-bold text-yellow-500 tracking-wider mb-2">ME</h2>
              <MainPlayerCard player={mockAlly}/>
            </div>

            {/* Right column: Enemies */}
            <div className="flex flex-col gap-2 items-end">
              <h2 className="text-sm font-bold text-red-400 tracking-wider mb-2">ENEMIES</h2>
              <div className="flex flex-col gap-3 items-end">
                <PlayerCard player={mockAlly}/>
                <PlayerCard player={mockAlly}/>
                <PlayerCard player={mockAlly}/>
                <PlayerCard player={mockAlly}/>
                <PlayerCard player={mockAlly}/>
              </div>
            </div>

          </section>

          {/* TIPS FEED SECTION */}
          <section className="mt-4">
            <TipFeed />
          </section>

          {/* RAW EVENTS SECTION */}
          <section>
            <EventTicker />
          </section>

        </main>
      </div>
  )
}

export default App