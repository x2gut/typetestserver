from datetime import datetime

from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import Base
from src.infrastructure.database.models.profile import Profile
from src.infrastructure.database.models.results_history import Result
from src.infrastructure.database.models.user_config import Config


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str | None] = mapped_column(String, nullable=True)
    google_id: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())

    profile: Mapped["Profile"] = relationship("Profile", back_populates="user")
    config: Mapped["Config"] = relationship("Config", back_populates="user")
    results: Mapped[list["Result"]] = relationship("Result", back_populates="user")
