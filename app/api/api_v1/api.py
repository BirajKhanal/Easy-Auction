from fastapi import APIRouter

from .endpoints import auction, user, login, category, sellable, cart, cartlog, shoppingsession

api_router = APIRouter()

api_router.include_router(auction.router, prefix="/auction", tags=["Auction"])
api_router.include_router(
    category.router, prefix="/category", tags=["Category"])
api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(login.router, prefix="/auth", tags=["Auth"])
api_router.include_router(sellable.router, prefix="/sellable", tags=["Sellable"])
api_router.include_router(cart.router, prefix="/cart", tags=["Cart"])
api_router.include_router(cartlog.router, prefix="/cartlog", tags=["Cart Log"])
api_router.include_router(shoppingsession.router, prefix="/shoppingsession", tags=["Shopping Session"])
