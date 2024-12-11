from pydantic import BaseModel


class SaveResult(BaseModel):
    user_id: int
    wpm: int
    accuracy: int
    mistakes: int
    mode: str
    time: int
    words: int
    language: str
