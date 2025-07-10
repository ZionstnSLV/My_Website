from flask import Flask
from .config import Config
from .extensions import db, bcrypt, login_manager
from .routes.auth import auth_bp
from .routes.main import main_bp
from .routes.product import product_bp
from .routes.cart import cart_bp # Akan dibuat nanti

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth') # Contoh prefix untuk auth
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(cart_bp, url_prefix='/cart')

    with app.app_context():
        db.create_all() # Buat tabel database jika belum ada

        # Optional: Tambahkan data dummy produk jika database kosong
        from .models import Product
        if Product.query.count() == 0:
            print("Adding dummy products...")
            dummy_products = [
                Product(name="Smartphone X Pro", price=8999000, image_url="https://placehold.co/300x200", description="Smartphone flagship dengan kamera terbaik di kelasnya.", category="Elektronik", stock=50),
                Product(name="Laptop Ultra Thin", price=12999000, image_url="https://placehold.co/300x200", description="Laptop ringan dengan performa tinggi dan baterai tahan lama.", category="Elektronik", stock=30),
                Product(name="Sepatu Olahraga Premium", price=1499000, image_url="https://placehold.co/300x200", description="Sepatu olahraga dengan teknologi terbaru untuk kenyamanan maksimal.", category="Fashion", stock=100),
                Product(name="Blender Multi Fungsi", price=899000, image_url="https://placehold.co/300x200", description="Blender dengan berbagai fungsi untuk kebutuhan dapur Anda.", category="Rumah Tangga", stock=75),
                Product(name="Smart TV 4K 55 Inci", price=7500000, image_url="https://placehold.co/300x200", description="Pengalaman menonton terbaik dengan resolusi 4K.", category="Elektronik", stock=20),
                Product(name="Headphone Nirkabel Bass", price=750000, image_url="https://placehold.co/300x200", description="Suara jernih dan bass mendalam, bebas kabel.", category="Elektronik", stock=120),
                Product(name="Kemeja Flanel Pria", price=250000, image_url="https://placehold.co/300x200", description="Kemeja flanel nyaman untuk gaya kasual.", category="Fashion", stock=150),
                Product(name="Dress Musim Panas Wanita", price=350000, image_url="https://placehold.co/300x200", description="Dress ringan dan stylish untuk musim panas.", category="Fashion", stock=80),
                Product(name="Set Peralatan Masak Anti Lengket", price=1200000, image_url="https://placehold.co/300x200", description="Lengkap dengan panci dan wajan anti lengket.", category="Rumah Tangga", stock=40),
                Product(name="Vacuum Cleaner Robotik", price=3000000, image_url="https://placehold.co/300x200", description="Membersihkan rumah secara otomatis.", category="Rumah Tangga", stock=15)
            ]
            db.session.add_all(dummy_products)
            db.session.commit()
            print("Dummy products added.")

    return app
