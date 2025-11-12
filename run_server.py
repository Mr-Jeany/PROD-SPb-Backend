#!/usr/bin/env python3
"""
Скрипт для запуска API сервера
"""

import os
import sys

import creating_tables
from app import app

if __name__ == '__main__':
    # Проверяем, существует ли база данных
    if not os.path.exists('main.db'):
        print("📦 Database not found. Creating tables and seeding data...")
        from creating_tables import *
        from seed_data import main as seed_main
        seed_main()
        print("✅ Database initialized!")
    
    print("🚀 Starting API server...")
    print("📍 Server will be available at: http://localhost:5000")
    print("📋 API endpoints:")
    print("   GET  /api/health - Health check")
    print("   GET  /api/items/search?name={query} - Search products")
    print("   GET  /api/items/scroll?offset={offset}&limit={limit} - Get products with pagination")
    print("   GET  /api/items/category?categoryId={id} - Get products by category ID")
    print("   GET  /api/items/category?categoryName={name} - Get products by category name")
    print("   GET  /api/categories - Get all categories")
    print("   POST /api/auth/register - Register new user")
    print("   POST /api/auth/login - Login user")
    print("   GET  /api/user/profile - Get user profile (requires auth)")
    print("\n🔑 Test credentials:")
    print("   Phone: +7 900 123 45 67")
    print("   Email: test@example.com")
    print("   Password: password123")
    print("\n" + "="*50)

    engine, db_path = creating_tables.get_engine_and_ensure_db("main.db")
    print(f"DB ready at: {db_path} (exists={db_path.exists()})")
    app.run(debug=True, host='0.0.0.0', port=8080)
