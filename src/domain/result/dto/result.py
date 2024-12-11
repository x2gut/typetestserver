from datetime import datetime

from src.domain.common.dto.base import DTO


class BaseResult(DTO):
    pass


class Result(BaseResult):
    id: int
    user_id: int
    wpm: int
    accuracy: int
    mistakes: int
    mode: str
    time: int
    words: int
    language: str
    created_at: datetime


class BestResult(BaseResult):
    username: str
    user_id: int
    wpm: int
    accuracy: int
    time: int
    words: int
    created_at: datetime


class StatisticTime(BaseResult):
    time_avg_15: float
    time_avg_30: float
    time_avg_60: float

    time_best_15: float
    time_best_30: float
    time_best_60: float


class StatisticWords(BaseResult):
    words_avg_25: float
    words_avg_50: float
    words_avg_100: float

    words_best_25: float
    words_best_50: float
    words_best_100: float


class ResultStatisticsOutput(BaseResult):
    time: StatisticTime
    words: StatisticWords
