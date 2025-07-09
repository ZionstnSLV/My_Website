   from flask import Blueprint, render_template, request, jsonify, session
   from ..models import User, Product
   from ..extensions import db
   from werkzeug.security import generate_password_hash, check_password_hash

   bp = Blueprint('user_routes', __name__)

   @bp.route('/')
   def index():
       return render_template('index.html')

   @bp.route('/api/register', methods=['POST'])
   def register():
       data = request.get_json()
       if not all(key in data for key in ['name', 'email', 'phone', 'password']):
           return jsonify({'error': 'Missing required fields'}), 400

       if User.query.filter_by(email=data['email']).first():
           return jsonify({'error': 'Email already registered'}), 400

       hashed_password = generate_password_hash(data['password'], method='sha256')
       new_user = User(
           name=data['name'],
           email=data['email'],
           phone=data['phone'],
           password=hashed_password
       )

       db.session.add(new_user)
       db.session.commit()

       session['user_id'] = new_user.id
       session['user_name'] = new_user.name

       return jsonify({
           'message': 'User  registered successfully',
           'user': {
               'id': new_user.id,
               'name': new_user.name,
               'email': new_user.email,
               'phone': new_user.phone
           }
       }), 201

   @bp.route('/api/login', methods=['POST'])
   def login():
       data = request.get_json()
       if not all(key in data for key in ['email', 'password']):
           return jsonify({'error': 'Email and password required'}), 400

       user = User.query.filter_by(email=data['email']).first()
       if not user or not check_password_hash(user.password, data['password']):
           return jsonify({'error': 'Invalid credentials'}), 401

       session['user_id'] = user.id
       session['user_name'] = user.name

       return jsonify({
           'message': 'Login successful',
           'user': {
               'id': user.id,
               'name': user.name,
               'email': user.email,
               'phone': user.phone
           }
       })
   