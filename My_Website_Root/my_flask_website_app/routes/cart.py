from flask import Blueprint, request, jsonify, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Product, CartItem

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add', methods=['POST'])
@login_required
def add_to_cart():
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity', 1)

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'success': False, 'message': 'Produk tidak ditemukan.'}), 404

    if product.stock < quantity:
        return jsonify({'success': False, 'message': 'Stok tidak mencukupi.'}), 400

    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f'{product.name} telah ditambahkan ke keranjang.', 'success')
    return jsonify({'success': True, 'message': 'Produk berhasil ditambahkan ke keranjang.'})

@cart_bp.route('/update', methods=['POST'])
@login_required
def update_cart_item():
    item_id = request.json.get('item_id')
    new_quantity = request.json.get('quantity')

    cart_item = CartItem.query.get(item_id)
    if not cart_item or cart_item.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Item keranjang tidak ditemukan.'}), 404
    
    if new_quantity <= 0:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item dihapus dari keranjang.', 'info')
        return jsonify({'success': True, 'message': 'Item dihapus dari keranjang.'})
    
    if cart_item.product.stock < new_quantity:
        return jsonify({'success': False, 'message': 'Stok tidak mencukupi.'}), 400

    cart_item.quantity = new_quantity
    db.session.commit()
    flash('Jumlah item keranjang diperbarui.', 'success')
    return jsonify({'success': True, 'message': 'Jumlah item keranjang diperbarui.'})

@cart_bp.route('/remove', methods=['POST'])
@login_required
def remove_from_cart():
    item_id = request.json.get('item_id')

    cart_item = CartItem.query.get(item_id)
    if not cart_item or cart_item.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Item keranjang tidak ditemukan.'}), 404
    
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item berhasil dihapus dari keranjang.', 'info')
    return jsonify({'success': True, 'message': 'Item berhasil dihapus dari keranjang.'})

@cart_bp.route('/items')
@login_required
def get_cart_items():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    items_data = []
    for item in cart_items:
        items_data.append({
            'id': item.id,
            'product_id': item.product.id,
            'name': item.product.name,
            'price': item.product.price,
            'image_url': item.product.image_url,
            'category': item.product.category,
            'quantity': item.quantity
        })
    return jsonify({'success': True, 'items': items_data})

@cart_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        return jsonify({'success': False, 'message': 'Keranjang belanja kosong.'}), 400

    total_amount = 0
    order_items = []
    
    try:
        for item in cart_items:
            if item.product.stock < item.quantity:
                db.session.rollback()
                return jsonify({'success': False, 'message': f'Stok {item.product.name} tidak mencukupi.'}), 400
            
            total_amount += item.product.price * item.quantity
            order_items.append(OrderItem(
                product_id=item.product.id,
                quantity=item.quantity,
                price_at_purchase=item.product.price
            ))
            item.product.stock -= item.quantity # Kurangi stok
            
        # Hitung ongkos kirim (contoh: 15000 jika total < 1jt, gratis jika >= 1jt)
        shipping_cost = 15000 if total_amount < 1000000 else 0
        final_total_amount = total_amount + shipping_cost

        new_order = Order(user_id=current_user.id, total_amount=final_total_amount, status='pending')
        db.session.add(new_order)
        db.session.flush() # Untuk mendapatkan ID order sebelum commit

        for order_item in order_items:
            order_item.order_id = new_order.id
            db.session.add(order_item)
        
        # Hapus item dari keranjang setelah checkout
        for item in cart_items:
            db.session.delete(item)

        db.session.commit()
        flash(f'Pesanan Anda berhasil dibuat! Total: Rp {final_total_amount:,.0f}', 'success')
        return jsonify({'success': True, 'message': 'Checkout berhasil!', 'order_id': new_order.id})

    except Exception as e:
        db.session.rollback()
        flash(f'Checkout gagal: {e}', 'danger')
        return jsonify({'success': False, 'message': f'Checkout gagal: {e}'}), 500
