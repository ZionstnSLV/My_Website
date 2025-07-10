from flask import Flask
from .config import Config
from .extensions import db
# from .routes.auth import auth_bp # Pastikan ini diimpor jika Anda menggunakannya
# from .routes.main import main_bp # Pastikan ini diimpor jika Anda menggunakannya
# from .routes.product import product_bp # Pastikan ini diimpor jika Anda menggunakannya
# from .routes.cart import cart_bp # Pastikan ini diimpor jika Anda menggunakannya

def create_app(): # <--- TIDAK ADA SPASI DI SINI
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    # bcrypt.init_app(app) # Jika Anda menggunakan bcrypt
    # login_manager.init_app(app) # Jika Anda menggunakan login_manager

    # Register Blueprints (sesuai dengan yang Anda definisikan di app.py sebelumnya)
    # app.register_blueprint(main_bp)
    # app.register_blueprint(auth_bp, url_prefix='/auth')
    # app.register_blueprint(product_bp, url_prefix='/products')
    # app.register_blueprint(cart_bp, url_prefix='/cart')

    # with app.app_context():
    #     db.create_all()
    #     # Optional: Tambahkan data dummy produk jika database kosong
    #     from .models import Product
    #     if Product.query.count() == 0:
    #         print("Adding dummy products...")
    #         # ... (kode dummy products)
    #         db.session.add_all(dummy_products)
    #         db.session.commit()
    #         print("Dummy products added.")

    return app
