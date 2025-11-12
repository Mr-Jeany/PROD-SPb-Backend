#!/usr/bin/env python3
"""
Скрипт для тестирования API
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_health():
    """Тест проверки здоровья API"""
    print("🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_search():
    """Тест поиска товаров"""
    print("🔍 Testing product search...")
    response = requests.get(f"{BASE_URL}/items/search?name=молоко")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} products")
    if data:
        print(f"First product: {data[0]['name']} - {data[0]['price']} руб.")
    print()

def test_scroll():
    """Тест пагинации товаров"""
    print("🔍 Testing product scrolling...")
    response = requests.get(f"{BASE_URL}/items/scroll?offset=0&limit=3")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} products")
    for product in data:
        print(f"  - {product['name']} - {product['price']} руб.")
    print()

def test_categories():
    """Тест получения категорий"""
    print("🔍 Testing categories...")
    response = requests.get(f"{BASE_URL}/categories")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} categories")
    for category in data:
        print(f"  - {category['name']} ({category['productCount']} товаров)")
    print()

def test_register():
    """Тест регистрации пользователя"""
    print("🔍 Testing user registration...")
    data = {
        "name": "Тест Тестович",
        "phoneOrEmail": "+7 999 888 77 66",
        "password": "test123456"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {result}")
    if result.get('success'):
        return result.get('token')
    return None

def test_login():
    """Тест входа пользователя"""
    print("🔍 Testing user login...")
    data = {
        "phoneOrEmail": "+7 900 123 45 67",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {result}")
    if result.get('success'):
        return result.get('token')
    return None

def test_profile(token):
    """Тест получения профиля пользователя"""
    if not token:
        print("❌ No token provided for profile test")
        return
    
    print("🔍 Testing user profile...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/user/profile", headers=headers)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {result}")
    print()

def test_category_products():
    """Тест получения товаров по категории"""
    print("🔍 Testing products by category...")
    response = requests.get(f"{BASE_URL}/items/category?categoryName=Молочные продукты")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} products in 'Молочные продукты'")
    for product in data[:3]:  # Показываем первые 3
        print(f"  - {product['name']} - {product['price']} руб.")
    print()

def main():
    """Основная функция тестирования"""
    print("🧪 API Testing Suite")
    print("=" * 50)
    
    try:
        # Базовые тесты
        test_health()
        test_search()
        test_scroll()
        test_categories()
        test_category_products()
        
        # Тесты аутентификации
        print("🔐 Testing authentication...")
        token = test_login()
        if token:
            test_profile(token)
        
        # Тест регистрации (может не работать если пользователь уже существует)
        print("🔐 Testing registration...")
        test_register()
        
        print("✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Make sure it's running on localhost:5000")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    main()
