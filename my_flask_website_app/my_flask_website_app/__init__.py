   from flask import Flask
   from .config import Config
   from .extensions import db

   def create_app():
       app = Flask(__name__)
       app.config.from_object(Config)

       db.init_app(app)

       # Import routes
       from .routes import user_routes
       app.register_blueprint(user_routes.bp)

       return app
   