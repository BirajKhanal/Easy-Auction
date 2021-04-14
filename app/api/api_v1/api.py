from fastapi import APIRouter

from .endpoints import auction, product, user, login, category, auctionable, sellable

api_router = APIRouter()

api_router.include_router(auction.router, prefix="/auction", tags=["Auction"])
api_router.include_router(
    product.router, prefix="/product", tags=["Product"])
api_router.include_router(
    category.router, prefix="/category", tags=["Category"])
api_router.include_router(
    auctionable.router, prefix="/auctionable", tags=["Auctionable"])
api_router.include_router(
    sellable.router, prefix="/sellable", tags=["Sellable"])
api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(login.router, prefix="/auth", tags=["Auth"])
