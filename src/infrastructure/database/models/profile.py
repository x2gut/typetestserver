import os

from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.infrastructure.database.base import Base


class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    avatar_path: Mapped[str] = mapped_column(
        String, default=os.path.join("assets", "uploads", "avatars", "base_avatar.png")
    )
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="profile")
