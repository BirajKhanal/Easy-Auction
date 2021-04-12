from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas import product as prodcutSchema


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 5):
    return db.query(Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: prodcutSchema.ProductCreate):
    name = product.name
    category = product.category
    reserv = product.reserv
    db_product = Product(name=name, description=product.description,
                         category=category, product_condition=product.product_condition, reserv=reserv)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
