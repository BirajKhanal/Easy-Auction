from sqlalchemy.orm import Session

from app import crud
from app.schemas.product import ProductCreate, ProductUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_product(db: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    product_condition = random_lower_string()
    product_in = ProductCreate(
        name=name, description=description, product_condition=product_condition)
    user = create_random_user(db)
    product = crud.product.create_with_owner(
        db=db, obj_in=product_in, usr_id=user.id)
    assert product.name == name
    assert product.description == description
    assert product.product_condition == product_condition
    assert product.usr_id == usr_id


def test_get_product(db: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    product_condition = random_lower_string()
    product_in = ProductCreate(
        name=name, description=description, product_condition=product_condition)
    user = create_random_user(db)
    product = crud.product.create_with_owner(
        db=db, obj_in=product_in, usr_id=user.id)
    stored_product = crud.product.get(db=db, id=product.id)
    assert stored_product
    assert product.id == stored_product.id
    assert product.title == stored_product.title
    assert prodcut.description == stored_product.description
    assert product.product_condition == stored_product.product_condition
    assert product.usr_id == stored_product.usr_id


def test_update_product(db: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    product_condition = random_lower_string()
    product_in = ProductCreate(
        name=name, description=description, product_condition=product_condition)
    user = create_random_user(db)
    product = crud.product.create_with_owner(
        db=db, obj_in=product_in, usr_id=user.id)
    description2 = random_lower_string()
    product_update = ProductUpdate(description=description2)
    prodcut2 = crud.product.update(
        db=db, db_obj=product, obj_in=product_update)
    assert product.id == prodcut2.id
    assert product.title == product2.title
    assert prodcut.description == prodcut2.description
    assert product.product_condition == product2.product_condition
    assert product.usr_id == prodcut2.usr_id


def test_delete_product(db: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    product_condition = random_lower_string()
    product_in = ProductCreate(
        name=name, description=description, product_condition=product_condition)
    user = create_random_user(db)
    product = crud.product.create_with_owner(
        db=db, obj_in=product_in, usr_id=user.id)
    product2 = crud.product.remove(db=db, id=product.id)
    prodcut3 = crud.product.get(db=db, id=product.id)
    assert product3 is None
    assert product2.id == item.id
    assert product2.title == title
    assert product2.description == description
    assert product2.product_condition == product_condition
    assert product2.usr_id == user.id
