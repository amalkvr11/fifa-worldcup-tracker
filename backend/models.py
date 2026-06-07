from pydantic import BaseModel
from typing import Optional


class Match(BaseModel):
    id: int
    team1: str
    team2: str
    team1_code: str
    team2_code: str
    team1_flag: str
    team2_flag: str
    group: str
    stage: str
    date_utc: str
    venue: str
    status: str
    score_team1: Optional[int] = None
    score_team2: Optional[int] = None
    favorite_count: int = 0


class Player(BaseModel):
    name: str
    number: int
    position: str
    rating: int
    photo: str


class Team(BaseModel):
    code: str
    name: str
    group: str
    flag: str


class FavoriteRequest(BaseModel):
    team_code: str


class MatchResponse(BaseModel):
    matches: list[Match]
    total: int


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


class PredictionRequest(BaseModel):
    team1_code: str
    team2_code: str


class LiveScoreUpdate(BaseModel):
    match_id: int
    score_team1: int
    score_team2: int
    minute: int
    event: str = ""
