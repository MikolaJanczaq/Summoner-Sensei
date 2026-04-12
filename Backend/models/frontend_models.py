from typing import Optional

from pydantic import BaseModel, Field

class KDAStats(BaseModel):
    kills: int
    deaths: int
    assists: int


class FrontendPlayer(BaseModel):
    champion_name: str = Field(alias="championName")
    level: int
    items: list[str]
    kda: KDAStats
    gold: Optional[float] = None
    is_me: bool = Field(alias="isMe")


class FrontendGameState(BaseModel):
    game_time: float = Field(alias="gameTime")
    me: FrontendPlayer
    allies: list[FrontendPlayer]
    enemies: list[FrontendPlayer]


