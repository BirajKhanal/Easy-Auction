from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from models import auctionModel
from schemas import auctionSchemas
from crud import auctionCrud
from database import SessionLocal, engine

auctionModel.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# apple
@app.post("/products/", response_model=auctionSchemas.Product)
def create_product(product: auctionSchemas.ProductCreate, db: Session = Depends(get_db)):
    return auctionCrud.create_product(db=db, product=product)


@app.get("/products", response_model=List[auctionSchemas.Product])
def read_products(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    products = auctionCrud.get_products(db, skip=skip, limit=limit)
    return products


@app.get("/products/{product_id}", response_model=auctionSchemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = auctionCrud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product Not Found")
    return db_product
