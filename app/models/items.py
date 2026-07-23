from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Model


class Item(Model):
    __tablename__= 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    stock_quantity: Mapped[int]