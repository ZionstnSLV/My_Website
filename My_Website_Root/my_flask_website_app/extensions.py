from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # Nama endpoint untuk halaman login
login_manager.login_message_category = 'info' # Kategori pesan flash

@login_manager.user_loader
def load_user(user_id):
    from .models import User # Import di sini untuk menghindari circular import
    return User.query.get(int(user_id))
