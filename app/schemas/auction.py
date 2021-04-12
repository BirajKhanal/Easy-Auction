from pydantic import BaseModel


class AuctionBase(BaseModel):
    selling_price: int


class AuctionCreate(AuctionBase):
    pass


class Auciton(AuctionBase):
    id: int
    product_id: int

    class Config:
        orm_mode = True
