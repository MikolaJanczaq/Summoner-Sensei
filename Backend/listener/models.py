from pydantic import BaseModel, Field


class Scores(BaseModel):
    kills: int
    deaths: int
    assists: int
    creep_score: int = Field(alias="creepScore")
    ward_score: float = Field(alias="wardScore")

class Item(BaseModel):
    id: int = Field(alias="itemID")
    name: str = Field(alias="displayName")


class Player(BaseModel):
    name: str = Field(alias="riotId")
    champion: str = Field(alias="championName")
    level: int
    items: list[Item]
    is_dead: bool = Field(alias="isDead")
    position: str
    team: str
    scores: Scores

class ActivePlayer(Player):
    champion_stats: dict = Field(alias="championStats")
    gold: float = Field(alias="currentGold")


class GameState(BaseModel):
    game_time: float
    me: ActivePlayer
    enemies: list[Player]
    allies: list[Player]
    last_event_id: int
    on_going: bool


class Event(BaseModel):
    id: int = Field(alias="EventID")
    name: str = Field(alias="EventName")
    time: float = Field(alias="EventTime")
    killer: str | None = Field(default=None, alias="KillerName")
    assisters: list[str] | None  = Field(default=None, alias="Assisters")
    victim: str | None = Field(default=None, alias="VictimName")
    # IF OBJECTIVE EVENTS
    dragon_type: str | None = Field(default=None, alias="DragonType")
    stolen: bool | None = Field(default=None, alias="Stolen")
    turret: str | None = Field(default=None, alias="TurretKilled")