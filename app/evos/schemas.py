from pydantic import BaseModel


class SCategory(BaseModel):
    name: str


class SRCategory(SCategory):
    id: int
