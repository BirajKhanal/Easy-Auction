from fastapi import FastAPI

from .routers import auction, products
from .models import auction

app = FastAPI()

auction.Base.metadata.create_all(bind=engine)

app.include_router(auction.router, prefix='/auction', tags=['auction'])
app.include_router(products.router, prefix='/product', tags=['product'])
