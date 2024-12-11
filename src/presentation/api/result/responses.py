import datetime
from typing import Dict, List

from pydantic import BaseModel

from src.domain.result.dto.result import Result as ResultDTO


class AverageResultStatisticResponse(BaseModel):
    time: Dict[str, int]
    word: Dict[str, int]


class ResultResponse(BaseModel):
    id: int
    user_id: int
    wpm: int
    accuracy: int
    mistakes: int
    mode: str
    time: int
    words: int
    language: str
    created_at: datetime.datetime


class HistoryResponse(BaseModel):
    total_items: int
    history: List[ResultDTO]
