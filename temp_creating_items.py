import csv
from io import StringIO
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import unicodedata

import yandexgpt
from db_types import Shops, ProductList  # Assuming you have these already defined

engine = create_engine("sqlite:///main.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Simulate your CSV input from yandexgpt.get_filtered_values()
csv_data = yandexgpt.get_filtered_values("example.csv")

# Step 1: Parse CSV
reader = csv.DictReader(StringIO(csv_data.strip()))
products = list(reader)

# Step 2: Generate item_id for each unique title
title_to_item_id = {}
next_item_id = 1

for product in products:
    title = product["title"]
    if title not in title_to_item_id:
        title_to_item_id[title] = next_item_id
        next_item_id += 1

# Step 3: Get shop name → id mapping from DB
shop_name_to_id = {
    shop.name: shop.id for shop in session.query(Shops).all()
}

# Step 4: Prepare ProductList entries
new_products = []


def normalize_partner_name(name):
    name = name.strip()
    name = unicodedata.normalize("NFKC", name)
    return name.replace("’", "'")

for product in products:
    title = product["title"]
    category = product["category"]

    partner = normalize_partner_name(product["partner"])
    shop_id = shop_name_to_id.get(partner)

    if shop_id is None:
        print(f"⚠️ Shop '{partner}' not found in DB, skipping.")
        continue

    new_product = ProductList(
        item_id=title_to_item_id[title],
        shop_id=shop_id,
        name=title,
        category=category,
        price=-1,
        image_url="nothing",
        in_stock=True
    )
    new_products.append(new_product)

# Step 5: Add and commit
session.add_all(new_products)
session.commit()
print(f"✅ Inserted {len(new_products)} products.")
