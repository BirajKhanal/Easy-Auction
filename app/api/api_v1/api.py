from fastapi import APIRouter

from .endpoints import auction, user, login, category

api_router = APIRouter()

api_router.include_router(auction.router, prefix="/auction", tags=["Auction"])
api_router.include_router(
    category.router, prefix="/category", tags=["Category"])
api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(login.router, prefix="/auth", tags=["Auth"])
