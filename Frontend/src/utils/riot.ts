const championNameExceptions: Record<string, string> = {
    "Wukong": "MonkeyKing",
    "Nunu & Willump": "Nunu",
    "Renata Glasc": "Renata",
    "Bel'Veth": "Belveth",
    "Cho'Gath": "Chogath",
    "Kai'Sa": "Kaisa",
    "Kha'Zix": "Khazix",
    "Kog'Maw": "KogMaw",
    "Rek'Sai": "RekSai",
    "Vel'Koz": "Velkoz",
    "Nunu": "Nunu",
    "Dr. Mundo": "DrMundo",
    "Dr Mundo": "DrMundo"
};

export const getDDragonChampionName = (name: string): string => {
    return championNameExceptions[name] || name.replace(/['\s\.]/g, '');
};