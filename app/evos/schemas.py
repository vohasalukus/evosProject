from pydantic import BaseModel

# Category Schema


class SCategory(BaseModel):
    name: str


class SRCategory(SCategory):
    id: int

# Dish Schema


class SDish(BaseModel):
    name: str
    price: int
    category_id: int
    cart_id: int | None = None


class SUDish(BaseModel):
    name: str | None = None
    price: int | None = None
    category_id: int | None = None
    cart_id: int | None = None


class SRDish(SDish):
    id: int
