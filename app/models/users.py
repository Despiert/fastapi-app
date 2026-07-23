from app.core.database import Model
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime

class User(Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    registered_at: Mapped[datetime] = mapped_column(default=func.now())

class UserArchive(Model):
    __tablename__ = 'user_archive'
    id: Mapped[int]
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]
    is_active: Mapped[bool]
    registered_at: Mapped[datetime]
    archive_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)