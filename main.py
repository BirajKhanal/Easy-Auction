from fastapi import Depends, FastAPI

from database import SessionLocal, engine
from .routers import auction, products


app = FastAPI()

app.include_router(auction.router, prefix='/auction', tags=['auction'])
app.include_router(products.router, prefix='/product', tags=['product'])
