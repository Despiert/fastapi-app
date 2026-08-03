from pydantic import BaseModel, Field, ConfigDict


class ItemAdd(BaseModel):
    name: str = Field(..., min_length=2)
    description: str | None = Field(default='No description')
    price: float = Field(ge=0)
    stock_quantity: int = Field(ge=0)
    model_config = ConfigDict(extra='forbid')


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock_quantity: int | None = None