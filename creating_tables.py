import random

from sqlalchemy.orm import Session

from db_types import Base, Orders, Shops, Categories, ProductList, Users, UserTokens
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import csv

def get_engine_and_ensure_db(db_filename: str = "main.db"):
    db_path = Path(__file__).resolve().parent / db_filename
    db_path.parent.mkdir(parents=True, exist_ok=True)  # ensure folder exists

    db_url = URL.create("sqlite", database=str(db_path))
    engine = create_engine(db_url, echo=True, future=True)

    if not db_path.exists():
        with engine.connect():
            pass
        Base.metadata.create_all(bind=engine)

        with Session(engine) as session:
            with open("categories.csv", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    category_ = Categories(
                        id=int(row[0]),
                        name=row[1],
                        icon_url=row[2],
                        color=row[3],
                        product_count=int(row[4])
                    )

                    session.add(category_)
                session.commit()

            with open("shops.csv", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    shop_ = Shops(
                        id=int(row[0]),
                        name=row[1],
                        delivery_types=row[2]
                    )
                    session.add(shop_)
                session.commit()

            with open("product_list.csv", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)

                for row in reader:
                    if random.randint(1, 10) == 1: continue # one in ten orders will be removed like for better visualisation
                    product_ = ProductList(
                        id=int(row[0]),
                        item_id=int(row[1]),
                        shop_id=int(row[2]),
                        category_id=int(row[3]),
                        name=row[4],
                        category=row[5],
                        price=round(float(row[6])*(1+random.randint(-10, 10)/100), 2),
                        original_price=float(row[7]) if row[7] != '' else None,
                        image_url=f"/static/images/{int(row[1])}.png",
                        description=row[9],
                        rating=round(float(row[10])*(1+random.randint(-10, 0)/100), 2),
                        reviews_count=random.randint(10, 1000),
                        in_stock=bool(row[12]),
                        discount=int(row[13]) if row[13] != '' else None,
                        tags=row[14]
                    )
                    session.add(product_)
                session.commit()


    return engine, db_path

# Usage
engine, db_path = get_engine_and_ensure_db("main.db")
print(f"DB ready at: {db_path} (exists={db_path.exists()})")
