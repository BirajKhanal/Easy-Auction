from sqlalchemy.orm import Session

from models import auctionModel
from schemas import auctionSchemas


def get_product(db: Session, product_id: int):
    return db.query(auctionModel.Product).filter(auctionModel.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 5):
    return db.query(auctionModel.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: auctionSchemas.ProductCreate):
    name = product.name
    category = product.category
    reserv = product.reserv
    db_product = auctionModel.Product(name=name, description=product.description, category=category, product_condition=product.product_condition, reserv=reserv)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
