from .extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False) # Akan disimpan sebagai hash
    # Tambahkan kolom lain jika diperlukan (misal: phone, address)
    
    # Relasi dengan Order (jika ada)
    orders = db.relationship('Order', backref='customer', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    stock = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"Product('{self.name}', '{self.price}')"

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))

    def __repr__(self):
        return f"CartItem(User: {self.user_id}, Product: {self.product_id}, Qty: {self.quantity})"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending') # e.g., pending, completed, cancelled

    items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f"Order('{self.id}', '{self.user_id}', '{self.total_amount}')"

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Float, nullable=False) # Harga saat dibeli

    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))

    def __repr__(self):
        return f"OrderItem(Order: {self.order_id}, Product: {self.product_id}, Qty: {self.quantity})"
