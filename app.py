from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker
from flask_swagger_ui import get_swaggerui_blueprint

import cart
import creating_tables
import orders
from db_types import Base, Shops, ProductList, Categories, Users, UserTokens
from datetime import datetime, timedelta
import json
import re
import secrets
import hashlib

app = Flask(__name__)
CORS(app)  # Enable CORS for mobile app

# Database setup
engine = create_engine("sqlite:///main.db", echo=False)
Session = sessionmaker(bind=engine)

# Helper functions
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    # Russian phone number pattern
    pattern = r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
    return re.match(pattern, phone) is not None

def authenticate_token(token):
    """Authenticate user by token"""
    session = Session()
    try:
        user_token = session.query(UserTokens).filter(
            and_(
                UserTokens.token == token,
                UserTokens.expires_at > datetime.utcnow()
            )
        ).first()
        
        if user_token:
            return user_token.user
        return None
    finally:
        session.close()

def require_auth(f):
    """Decorator to require authentication"""
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'success': False, 'message': 'Токен авторизации не предоставлен'}), 401
        
        token = auth_header.split(' ')[1]
        user = authenticate_token(token)
        if not user:
            return jsonify({'success': False, 'message': 'Недействительный токен авторизации'}), 401
        
        return f(user, *args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# API Endpoints

@app.route('/api/items/search', methods=['GET'])
def get_items_by_search():
    """GET ItemsBySearch(String name)"""
    try:
        name = request.args.get('name', '').strip()
        if not name:
            return jsonify({'success': False, 'message': 'Параметр name обязателен'}), 400
        
        session = Session()
        try:
            products = session.query(ProductList).filter(
                and_(
                    ProductList.in_stock == True,
                    or_(
                        ProductList.name.ilike(f'%{name}%'),
                        ProductList.description.ilike(f'%{name}%'),
                        ProductList.tags.ilike(f'%{name}%')
                    )
                )
            ).all()
            
            result = []
            for product in products:
                tags = []
                if product.tags:
                    try:
                        tags = json.loads(product.tags)
                    except:
                        tags = []
                
                result.append({
                    'id': product.item_id,
                    'name': product.name,
                    'price': float(product.price),
                    'originalPrice': float(product.original_price) if product.original_price else None,
                    'imageUrl': product.image_url or '',
                    'category': product.category,
                    'description': product.description or '',
                    'rating': float(product.rating),
                    'reviewsCount': product.reviews_count,
                    'isInStock': product.in_stock,
                    'discount': product.discount,
                    'tags': tags,
                    "shopId": product.shop_id
                })
            
            return jsonify(result)
        finally:
            session.close()
    except Exception as e:
        return jsonify({'success': False, 'message': f'Ошибка поиска: {str(e)}'}), 500

@app.route('/api/items/scroll', methods=['GET'])
def get_items_scrolling():
    """GET ItemsScrolling() - list(json, len = 6)"""
    try:
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 6))
        
        session = Session()
        try:
            products = session.query(ProductList).filter(
                ProductList.in_stock == True
            ).offset(offset).limit(limit).all()
            
            result = []
            for product in products:
                tags = []
                if product.tags:
                    try:
                        tags = json.loads(product.tags)
                    except:
                        tags = []
                
                result.append({
                    'id': product.item_id,
                    'name': product.name,
                    'price': float(product.price),
                    'originalPrice': float(product.original_price) if product.original_price else None,
                    'imageUrl': product.image_url or '',
                    'category': product.category,
                    'description': product.description or '',
                    'rating': float(product.rating),
                    'reviewsCount': product.reviews_count,
                    'isInStock': product.in_stock,
                    'discount': product.discount,
                    'tags': tags,
                    "shopId": product.shop_id
                })
            
            return jsonify(result)
        finally:
            session.close()
    except Exception as e:
        return jsonify({'success': False, 'message': f'Ошибка загрузки товаров: {str(e)}'}), 500

@app.route('/api/items/category', methods=['GET'])
def get_items_by_category():
    """GET ItemsByCat(Int index\\ string name)"""
    try:
        category_id = request.args.get('categoryId')
        category_name = request.args.get('categoryName')
        
        if not category_id and not category_name:
            return jsonify({'success': False, 'message': 'Необходимо указать categoryId или categoryName'}), 400
        
        session = Session()
        try:
            query = session.query(ProductList).filter(ProductList.in_stock == True)
            
            if category_id:
                query = query.filter(ProductList.category_id == int(category_id))
            elif category_name:
                query = query.filter(ProductList.category.ilike(f'%{category_name}%'))
            
            products = query.all()
            
            result = []
            for product in products:
                tags = []
                if product.tags:
                    try:
                        tags = json.loads(product.tags)
                    except:
                        tags = []
                
                result.append({
                    'id': product.item_id,
                    'name': product.name,
                    'price': float(product.price),
                    'originalPrice': float(product.original_price) if product.original_price else None,
                    'imageUrl': product.image_url or '',
                    'category': product.category,
                    'description': product.description or '',
                    'rating': float(product.rating),
                    'reviewsCount': product.reviews_count,
                    'isInStock': product.in_stock,
                    'discount': product.discount,
                    'tags': tags,
                    "shopId": product.shop_id
                })
            
            return jsonify(result)
        finally:
            session.close()
    except Exception as e:
        return jsonify({'success': False, 'message': f'Ошибка загрузки товаров по категории: {str(e)}'}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """GET all categories"""
    try:
        session = Session()
        try:
            categories = session.query(Categories).all()
            
            result = []
            for category in categories:
                result.append({
                    'id': category.id,
                    'name': category.name,
                    'iconUrl': category.icon_url or '',
                    'color': category.color,
                    'productCount': category.product_count
                })
            
            return jsonify(result)
        finally:
            session.close()
    except Exception as e:
        return jsonify({'success': False, 'message': f'Ошибка загрузки категорий: {str(e)}'}), 500

@app.route('/api/auth/register', methods=['POST'])
def register_user():
    """POST NewUser(String name, string phone\\mail, string password)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Данные не предоставлены'}), 400
        
        name = data.get('name', '').strip()
        phone_or_email = data.get('phoneOrEmail', '').strip()
        password = data.get('password', '').strip()
        
        # Validation
        if not name or len(name) < 2:
            return jsonify({'success': False, 'message': 'Имя должно содержать минимум 2 символа'}), 400
        
        if not phone_or_email:
            return jsonify({'success': False, 'message': 'Телефон или email обязательны'}), 400
        
        if not password or len(password) < 6:
            return jsonify({'success': False, 'message': 'Пароль должен содержать минимум 6 символов'}), 400
        
        # Check if phone or email
        is_email = is_valid_email(phone_or_email)
        is_phone = is_valid_phone(phone_or_email)
        
        if not is_email and not is_phone:
            return jsonify({'success': False, 'message': 'Неверный формат телефона или email'}), 400
        
        session = Session()
        try:
            # Check if user already exists
            existing_user = None
            if is_email:
                existing_user = session.query(Users).filter(Users.email == phone_or_email).first()
            else:
                existing_user = session.query(Users).filter(Users.phone == phone_or_email).first()
            
            if existing_user:
                return jsonify({'success': False, 'message': 'Пользователь с таким телефоном или email уже существует'}), 400
            
            # Create new user
            password_hash = UserTokens.hash_password(password)
            new_user = Users(
                name=name,
                email=phone_or_email if is_email else None,
                phone=phone_or_email if is_phone else None,
                password_hash=password_hash
            )
            
            session.add(new_user)
            session.commit()
            
            # Generate token
            token = UserTokens.generate_token()
            expires_at = datetime.utcnow() + timedelta(days=30)
            
            user_token = UserTokens(
                user_id=new_user.id,
                token=token,
                expires_at=expires_at
            )
            
            session.add(user_token)
            session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Пользователь успешно зарегистрирован',
                'token': token
            })
        finally:
            session.close()
    except Exception as e:
        return jsonify({'success': False, 'message': f'Ошибка регистрации: {str(e)}'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login_user():
    """GET AuthorizationUser(string phone\\mail, string password)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Данные не предоставлены'}), 400
        
        phone_or_email = data.get('phoneOrEmail', '').strip()
        password = data.get('password', '').strip()
        
        if not phone_or_email or not password:
            return jsonify({'success': False, 'message': 'Телефон/email и пароль обязательны'}), 400
        
        session = Session()
        try:
            # Find user
            user = None
            if is_valid_email(phone_or_email):
                user = session.query(Users).filter(Users.email == phone_or_email).first()
            elif is_valid_phone(phone_or_email):
                user = session.query(Users).filter(Users.phone == phone_or_email).first()
            else:
                return jsonify({'success': False, 'message': 'Неверный формат телефона или email'}), 400
            
            if not user:
                return jsonify({'success': False, 'message': 'Пользователь не найден'}), 401
            
            # Check password
            password_hash = UserTokens.hash_password(password)
            if user.password_hash != password_hash:
                return jsonify({'success': False, 'message': 'Неверный пароль'}), 401
            
            if not user.is_active:
                return jsonify({'success': False, 'message': 'Аккаунт заблокирован'}), 401
            
            # Generate new token
            token = UserTokens.generate_token()
            expires_at = datetime.utcnow() + timedelta(days=30)
            
            user_token = UserTokens(
                user_id=user.id,
                token=token,
                expires_at=expires_at
            )
            
            session.add(user_token)
            session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Успешная авторизация',
                'token': token
            })
        finally:
            session.close()
    except Exception as e:
        return jsonify({'success': False, 'message': f'Ошибка авторизации: {str(e)}'}), 500

@app.route('/api/user/profile', methods=['GET'])
@require_auth
def get_user_profile(user):
    """GET user profile"""
    try:
        return jsonify({
            'id': user.id,
            'name': user.name,
            'phone': user.phone,
            'email': user.email,
            'address': user.address,
            'avatarUrl': user.avatar_url
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Ошибка получения профиля: {str(e)}'}), 500

# Root endpoint
@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'PRODOne API Server',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'search': '/api/items/search?name={query}',
            'products': '/api/items/scroll?offset={offset}&limit={limit}',
            'categories': '/api/categories',
            'register': '/api/auth/register',
            'login': '/api/auth/login'
        }
    })

@app.route("/api/orders/create", methods=["POST"])
@require_auth
def create_order(user):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"successs": False, "message": "Нет данных."}), 400


        items = data.get('items', '')
        user_id = user.id

        return jsonify({"id": orders.create_order_row(engine, items, user_id, "created"), "items": items, "user_id": user_id})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Ошибка создания заказа: {str(e)}'}), 500


@app.route("/api/orders/get", methods=["GET"])
@require_auth
def get_order(user):
    try:
        order_id = request.args.get('orderId')
        if not order_id:
            return jsonify({'success': False, 'message': 'Параметр orderId обязателен'}), 400

        found_order = orders.get_order_object(engine, order_id=order_id)

        if found_order.user_id == user.id:
            return_value = {
                "id": found_order.id,
                "items": found_order.list_of_unique_ids,
                "user_id": found_order.user_id,
                "status": found_order.status,
                "created_at": found_order.created_at
            }

            return jsonify(return_value)
        else:
            return jsonify({'success': False, 'message': 'У вас нет доступа к этому заказу.'}), 403

    except Exception as e:
        return jsonify({'success': False, 'message': f'Ошибка получения заказа: {str(e)}'}), 500

@app.route("/api/orders/all", methods=["GET"])
@require_auth
def get_all_orders(user):
    try:
        user_orders = orders.get_user_orders(engine, user)
        result = []
        for order in user_orders:
            result.append(order.id)

        return jsonify({"userOrdersIds": result})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Ошибка получения заказа: {str(e)}'}), 500

@app.route("/api/cart/add", methods=["POST"])
@require_auth
def add_item_to_cart(user):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"successs": False, "message": "Нет данных."}), 400

        item = data.get('item')

        c = cart.add_to_cart(engine, user.id, item)



        return jsonify({'success': True, 'message': f"Successfully added new item to the cart.", "cart": c})


    except Exception as e:
        return jsonify({'success': False, 'message': f'Ошибка добавления в корзину: {str(e)}'}), 500


@app.route("/api/cart/remove", methods=["POST"])
@require_auth
def remove_item_from_cart(user):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"successs": False, "message": "Нет данных."}), 400

        item = data.get('item')

        c = cart.remove_from_cart(engine, user.id, int(item))



        return jsonify({'success': True, 'message': f"Successfully remvoed item to the cart. {c}", "cart": c})


    except Exception as e:
        return jsonify({'success': False, 'message': f'Ошибка удаления из корзины: {str(e)}'}), 500

@app.route("/api/cart/info", methods=["GET"])
@require_auth
def get_cart(user):
    try:
        c = cart.get_cart(engine, user.id)

        return jsonify({"items": c})


    except Exception as e:
        return jsonify({'success': False, 'message': f'Ошибка в получении значения: {str(e)}'}), 500


@app.route("/api/cart/clear", methods=["POST"])
@require_auth
def clear_cart(user):
    try:

        c = cart.clear_cart(engine, user.id)



        return jsonify({'success': True, 'message': f"Successfully cleared the cart.", "cart": c})


    except Exception as e:
        return jsonify({'success': False, 'message': f'Ошибка добавления в корзину: {str(e)}'}), 500


# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'message': 'API is running'})


SWAGGER_URL = "/api/docs"                 # Swagger UI endpoint
API_URL = "/static/openapi.yaml"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "PRODOne API"
    },
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    engine, db_path = creating_tables.get_engine_and_ensure_db("main.db")
    print(f"DB ready at: {db_path} (exists={db_path.exists()})")
    app.run(debug=True, host='0.0.0.0', port=8080)
