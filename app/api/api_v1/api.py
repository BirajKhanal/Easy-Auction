from fastapi import APIRouter

from .endpoints import auction, product, user, login

api_router = APIRouter()

api_router.include_router(auction.router, prefix="/auction", tags=["auction"])
api_router.include_router(
    product.router, prefix="/product", tags=["product"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(login.router, prefix="/auth", tags=["auth"])
