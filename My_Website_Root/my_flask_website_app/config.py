import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key_yang_sangat_panjang_dan_acak' # Ganti ini di produksi!
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db' # Contoh SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Tambahkan konfigurasi lain jika diperlukan
