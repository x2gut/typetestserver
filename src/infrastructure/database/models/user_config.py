from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import Base


class Config(Base):
    __tablename__ = "config"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    theme: Mapped[str] = mapped_column(String, default="base")
    config: Mapped[JSONB] = mapped_column(
        JSONB,
        nullable=False,
        default=lambda: {
            "layout": "english",
            "lang": "english",
            "mode": "time",
            "time": 60,
            "words": 50,
            "keyboard": {"show": False, "responsive": False},
            "soundOnPress": False,
            "caretType": "default",
            "caretRainbow": False,
            "randomTheme": False,
            "themesSidebar": True,
            "wordsHistory": True,
        },
    )

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="config")
