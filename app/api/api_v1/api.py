from fastapi import APIRouter

from .endpoints import auction, product

api_router = APIRouter()

api_router.include_router(auction.router, prefix="/auction", tags=["auction"])
api_router.include_router(
    product.router, prefix="/product", tags=["product"])
