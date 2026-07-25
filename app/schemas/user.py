from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime


class UserAdd(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=30)
    model_config = ConfigDict(extra='forbid')

class UserGet(BaseModel):
    id: int
    username: str
    email: EmailStr
    registered_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserDel(BaseModel):
    message: str
    user_id: int

class UserPatch(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    model_config = ConfigDict(extra='forbid')

class UserArchiveAdd(BaseModel):
    id: int
    username: str
    password: str
    email: EmailStr
    is_active: bool
    registered_at: datetime
    model_config = ConfigDict(from_attributes=True)
