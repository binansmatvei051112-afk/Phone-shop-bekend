from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: int

class Cases(BaseModel):
    name: str
    material: str
    price: int
    Items_id: int