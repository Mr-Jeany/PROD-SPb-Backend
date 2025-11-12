import ast
import json

from flask import jsonify
from sqlalchemy import Text
from sqlalchemy.orm import Session

from db_types import Users


def add_to_cart(engine, user_id: int, item_id):
    with Session(engine) as session:
        found_user = session.get(Users, user_id)
        cart = json.loads(found_user.cart) if found_user.cart else []
        if type(item_id) == list:
            cart += item_id
        else:
            cart.append(item_id)

        found_user.cart = json.dumps(cart)

        session.commit()

        return cart

def remove_from_cart(engine, user_id: int, item_id: int):
    with Session(engine) as session:
        found_user = session.get(Users, user_id)
        cart = json.loads(found_user.cart) if found_user.cart else []
        cart.remove(item_id)

        found_user.cart = json.dumps(cart)

        session.commit()

        return cart

def get_cart(engine, user_id: int):
    with Session(engine) as session:
        found_user = session.get(Users, user_id)
        cart = json.loads(found_user.cart) if found_user.cart else []

        session.commit()

        return cart

def clear_cart(engine, user_id: int):
    with Session(engine) as session:
        found_user = session.get(Users, user_id)
        cart = []
        session.commit()

        return cart