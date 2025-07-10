from flask import Blueprint, render_template
from ..models import Product # Import model Product

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/home')
def home():
    products = Product.query.all() # Ambil semua produk dari database
    return render_template('index.html', products=products)
