import json

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DECIMAL, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

from db_types import Shops, ProductList

engine = create_engine("sqlite:///main.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

new_shops = [
    Shops(name="ВкусВилл", dilevery_types=json.dumps(["take-away", "self courier"])),
    # Shops(name="Лента", dilevery_types=json.dumps(["self courier"])),
    # Shops(name="О'кей", dilevery_types=json.dumps(["take-away"])),
    # Shops(name="Магнит", dilevery_types=json.dumps(["take-away", "self courier"])),
    # Shops(name="Перекрёсток", dilevery_types=json.dumps(["take-away", "self courier"]))
    ]

session.add_all(new_shops)

session.commit()
