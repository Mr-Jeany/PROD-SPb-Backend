#!/usr/bin/env python3
"""
Скрипт для заполнения базы данных тестовыми данными
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_types import Base, Shops, ProductList, Categories, Users, UserTokens
import json
import random
from datetime import datetime, timedelta

# Database setup
engine = create_engine("sqlite:///main.db", echo=False)
Session = sessionmaker(bind=engine)

def seed_categories():
    """Создание категорий"""
    session = Session()
    try:
        categories_data = [
            {"name": "Молочные продукты", "color": "#4CAF50", "icon_url": "https://example.com/milk.png"},
            {"name": "Мясо и птица", "color": "#E91E63", "icon_url": "https://example.com/meat.png"},
            {"name": "Овощи и фрукты", "color": "#8BC34A", "icon_url": "https://example.com/vegetables.png"},
            {"name": "Хлеб и выпечка", "color": "#FF9800", "icon_url": "https://example.com/bread.png"},
            {"name": "Напитки", "color": "#2196F3", "icon_url": "https://example.com/drinks.png"},
            {"name": "Сладости", "color": "#9C27B0", "icon_url": "https://example.com/sweets.png"},
            {"name": "Замороженные", "color": "#00BCD4", "icon_url": "https://example.com/frozen.png"},
            {"name": "Консервы", "color": "#795548", "icon_url": "https://example.com/canned.png"},
        ]
        
        for cat_data in categories_data:
            category = Categories(
                name=cat_data["name"],
                color=cat_data["color"],
                icon_url=cat_data["icon_url"],
                product_count=0
            )
            session.add(category)
        
        session.commit()
        print("✅ Categories created")
    finally:
        session.close()

def seed_shops():
    """Создание магазинов"""
    session = Session()
    try:
        shops_data = [
            {"name": "ВкусВилл", "delivery_types": ["take-away", "self courier"]},
            {"name": "Лента", "delivery_types": ["self courier"]},
            {"name": "О'кей", "delivery_types": ["take-away"]},
            {"name": "Магнит", "delivery_types": ["take-away", "self courier"]},
            {"name": "Перекрёсток", "delivery_types": ["take-away", "self courier"]}
        ]
        
        for shop_data in shops_data:
            shop = Shops(
                name=shop_data["name"],
                delivery_types=json.dumps(shop_data["delivery_types"])
            )
            session.add(shop)
        
        session.commit()
        print("✅ Shops created")
    finally:
        session.close()

def seed_products():
    """Создание товаров"""
    session = Session()
    try:
        # Get categories and shops
        categories = session.query(Categories).all()
        shops = session.query(Shops).all()
        
        if not categories or not shops:
            print("❌ No categories or shops found. Run seed_categories() and seed_shops() first.")
            return
        
        products_data = [
            # Молочные продукты
            {"name": "Молоко 3.2%", "category": "Молочные продукты", "price": 89, "original_price": 120, "description": "Свежее коровье молоко", "rating": 4.5, "reviews_count": 128, "discount": 26, "tags": ["молочные", "свежие"]},
            {"name": "Сыр Гауда", "category": "Молочные продукты", "price": 250, "description": "Голландский сыр", "rating": 4.8, "reviews_count": 67, "tags": ["сыр", "голландский"]},
            {"name": "Йогурт натуральный", "category": "Молочные продукты", "price": 65, "description": "Без добавок", "rating": 4.1, "reviews_count": 92, "tags": ["йогурт", "натуральный"]},
            {"name": "Творог 5%", "category": "Молочные продукты", "price": 120, "description": "Домашний творог", "rating": 4.3, "reviews_count": 156, "tags": ["творог", "домашний"]},
            {"name": "Сметана 20%", "category": "Молочные продукты", "price": 85, "description": "Деревенская сметана", "rating": 4.6, "reviews_count": 89, "tags": ["сметана", "деревенская"]},
            
            # Мясо и птица
            {"name": "Куриная грудка", "category": "Мясо и птица", "price": 180, "description": "Свежая куриная грудка", "rating": 4.6, "reviews_count": 203, "tags": ["курица", "грудка"]},
            {"name": "Говядина", "category": "Мясо и птица", "price": 450, "description": "Свежая говядина", "rating": 4.7, "reviews_count": 134, "tags": ["говядина", "свежая"]},
            {"name": "Свинина", "category": "Мясо и птица", "price": 320, "description": "Свежая свинина", "rating": 4.4, "reviews_count": 98, "tags": ["свинина", "свежая"]},
            {"name": "Индейка", "category": "Мясо и птица", "price": 280, "description": "Филе индейки", "rating": 4.5, "reviews_count": 76, "tags": ["индейка", "филе"]},
            
            # Овощи и фрукты
            {"name": "Яблоки Гренни Смит", "category": "Овощи и фрукты", "price": 120, "description": "Свежие зеленые яблоки", "rating": 4.7, "reviews_count": 156, "tags": ["яблоки", "зеленые"]},
            {"name": "Морковь", "category": "Овощи и фрукты", "price": 35, "description": "Свежая морковь", "rating": 4.3, "reviews_count": 78, "tags": ["морковь", "свежая"]},
            {"name": "Бананы", "category": "Овощи и фрукты", "price": 80, "description": "Спелые бананы", "rating": 4.5, "reviews_count": 145, "tags": ["бананы", "спелые"]},
            {"name": "Помидоры", "category": "Овощи и фрукты", "price": 150, "description": "Свежие помидоры", "rating": 4.4, "reviews_count": 112, "tags": ["помидоры", "свежие"]},
            {"name": "Огурцы", "category": "Овощи и фрукты", "price": 90, "description": "Свежие огурцы", "rating": 4.2, "reviews_count": 87, "tags": ["огурцы", "свежие"]},
            
            # Хлеб и выпечка
            {"name": "Хлеб Бородинский", "category": "Хлеб и выпечка", "price": 45, "description": "Традиционный ржаной хлеб", "rating": 4.2, "reviews_count": 89, "tags": ["хлеб", "ржаной"]},
            {"name": "Булочки с маком", "category": "Хлеб и выпечка", "price": 25, "description": "Свежие булочки", "rating": 4.0, "reviews_count": 45, "tags": ["булочки", "мак"]},
            {"name": "Круассаны", "category": "Хлеб и выпечка", "price": 35, "description": "Французские круассаны", "rating": 4.3, "reviews_count": 67, "tags": ["круассаны", "французские"]},
            
            # Напитки
            {"name": "Кофе Арабика", "category": "Напитки", "price": 350, "description": "Молотый кофе", "rating": 4.9, "reviews_count": 45, "tags": ["кофе", "арабика"]},
            {"name": "Чай Эрл Грей", "category": "Напитки", "price": 120, "description": "Черный чай с бергамотом", "rating": 4.6, "reviews_count": 78, "tags": ["чай", "черный"]},
            {"name": "Сок апельсиновый", "category": "Напитки", "price": 95, "description": "100% апельсиновый сок", "rating": 4.4, "reviews_count": 123, "tags": ["сок", "апельсиновый"]},
            
            # Сладости
            {"name": "Шоколад Милка", "category": "Сладости", "price": 85, "original_price": 110, "description": "Молочный шоколад", "rating": 4.4, "reviews_count": 234, "discount": 23, "tags": ["шоколад", "молочный"]},
            {"name": "Печенье Орео", "category": "Сладости", "price": 120, "description": "Печенье с кремом", "rating": 4.7, "reviews_count": 189, "tags": ["печенье", "крем"]},
            {"name": "Конфеты Рафаэлло", "category": "Сладости", "price": 180, "description": "Кокосовые конфеты", "rating": 4.8, "reviews_count": 156, "tags": ["конфеты", "кокос"]},
        ]
        
        item_id = 1
        for product_data in products_data:
            # Find category
            category = next((c for c in categories if c.name == product_data["category"]), None)
            if not category:
                continue
            
            # Create product for each shop
            for shop in shops:
                product = ProductList(
                    item_id=item_id,
                    shop_id=shop.id,
                    category_id=category.id,
                    name=product_data["name"],
                    category=product_data["category"],
                    price=product_data["price"],
                    original_price=product_data.get("original_price"),
                    image_url=f"https://example.com/images/{item_id}.jpg",
                    description=product_data["description"],
                    rating=product_data["rating"],
                    reviews_count=product_data["reviews_count"],
                    in_stock=True,
                    discount=product_data.get("discount"),
                    tags=json.dumps(product_data["tags"])
                )
                session.add(product)
                item_id += 1
        
        # Update product counts for categories
        for category in categories:
            count = session.query(ProductList).filter(ProductList.category_id == category.id).count()
            category.product_count = count
        
        session.commit()
        print(f"✅ Products created (total: {item_id - 1})")
    finally:
        session.close()

def seed_test_user():
    """Создание тестового пользователя"""
    session = Session()
    try:
        # Check if user already exists
        existing_user = session.query(Users).filter(Users.phone == "+7 900 123 45 67").first()
        if existing_user:
            print("✅ Test user already exists")
            return
        
        # Create test user
        password_hash = UserTokens.hash_password("password123")
        user = Users(
            name="Тестовый Пользователь",
            phone="+7 900 123 45 67",
            email="test@example.com",
            password_hash=password_hash,
            address="Москва, ул. Тестовая, д. 1"
        )
        session.add(user)
        session.commit()
        
        # Create token
        token = UserTokens.generate_token()
        expires_at = datetime.utcnow() + timedelta(days=30)
        
        user_token = UserTokens(
            user_id=user.id,
            token=token,
            expires_at=expires_at
        )
        session.add(user_token)
        session.commit()
        
        print(f"✅ Test user created")
        print(f"   Phone: +7 900 123 45 67")
        print(f"   Email: test@example.com")
        print(f"   Password: password123")
        print(f"   Token: {token}")
    finally:
        session.close()

def main():
    """Основная функция для заполнения базы данных"""
    print("🌱 Seeding database...")
    
    # Create tables if they don't exist
    Base.metadata.create_all(engine)
    
    # Seed data
    seed_categories()
    seed_shops()
    seed_products()
    seed_test_user()
    
    print("🎉 Database seeding completed!")

if __name__ == "__main__":
    main()
