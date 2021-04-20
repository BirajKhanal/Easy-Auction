import random
from sqlalchemy.orm import Session

from app.models.product import Category, ProductCondition
from app.crud.product import category as crud_category
from app.schemas.category import CategoryCreate

from app.tests.utils.utils import random_lower_string


def create_random_category(
    db: Session
) -> Category:
    name = random_lower_string()
    obj_in = CategoryCreate(name=name)
    return crud_category.create(db=db, obj_in=obj_in)


def random_product_condition():
    return random.choice([ProductCondition.BEST, ProductCondition.BRAND_NEW,
                          ProductCondition.GOOD, ProductCondition.POOR])
