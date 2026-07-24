from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class UserAdd(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: Annotated[str, MinLen(8), MaxLen(30)]

class UserGet(BaseModel):
    username: str
    email: EmailStr
    registered_at: datetime

class UserDel(BaseModel):
    message: str
    user_id: int

class UserPatch(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None

