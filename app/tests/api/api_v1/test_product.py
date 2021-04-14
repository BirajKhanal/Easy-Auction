from sqlalchemy.orm import Session

from app import crud
from app.schemas.category import CategoryCreate
from app.schemas.product import ProductCreate, ProductUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string
