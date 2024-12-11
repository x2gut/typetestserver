from datetime import datetime

from sqlalchemy import Integer, ForeignKey, Float, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import Base


class Result(Base):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    wpm: Mapped[int] = mapped_column(Integer)
    accuracy: Mapped[float] = mapped_column(Float)
    mistakes: Mapped[int] = mapped_column(Integer)
    time: Mapped[int] = mapped_column(Integer)
    words: Mapped[int] = mapped_column(Integer)
    mode: Mapped[str] = mapped_column(String)
    language: Mapped[str] = mapped_column(String)

    created_at: Mapped[datetime] = mapped_column(default=func.now().op("AT TIME ZONE")("UTC"))

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="results", uselist=True)
