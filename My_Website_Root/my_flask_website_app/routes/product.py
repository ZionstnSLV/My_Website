from flask import Blueprint, render_template, abort
from ..models import Product

product_bp = Blueprint('product', __name__)

@product_bp.route('/<int:product_id>')
def detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product) # Anda perlu membuat template product_detail.html
