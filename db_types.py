from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DECIMAL, Boolean, Float, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import hashlib
import secrets

Base = declarative_base()

class Shops(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    delivery_types = Column(Text)  # Fixed typo: dilevery -> delivery
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    products = relationship("ProductList", back_populates="shop")

class Categories(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    icon_url = Column(String)
    color = Column(String, default="#4CAF50")
    product_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    products = relationship("ProductList", back_populates="category_obj")

class ProductList(Base):
    __tablename__ = "product_list"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer)
    shop_id = Column(Integer, ForeignKey("shops.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    name = Column(String, nullable=False)
    category = Column(String)  # Keep for backward compatibility
    price = Column(DECIMAL(10, 2), nullable=False)
    original_price = Column(DECIMAL(10, 2))
    image_url = Column(String)
    description = Column(Text)
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    in_stock = Column(Boolean, default=True)
    discount = Column(Integer)  # Percentage discount
    tags = Column(Text)  # JSON string of tags
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    shop = relationship("Shops", back_populates="products")
    category_obj = relationship("Categories", back_populates="products")

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String, nullable=False)
    address = Column(Text)
    avatar_url = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cart = Column(Text)
    
    # Relationships
    tokens = relationship("UserTokens", back_populates="user")

class UserTokens(Base):
    __tablename__ = "user_tokens"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("Users", back_populates="tokens")
    
    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    list_of_unique_ids = Column(Text)
    user_id = Column(Integer)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)