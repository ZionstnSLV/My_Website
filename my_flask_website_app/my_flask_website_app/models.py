   from .extensions import db

   class User(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       name = db.Column(db.String(100), nullable=False)
       email = db.Column(db.String(100), unique=True, nullable=False)
       phone = db.Column(db.String(20), nullable=False)
       password = db.Column(db.String(200), nullable=False)

       def __repr__(self):
           return f'<User  {self.name}>'

   class Product(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       name = db.Column(db.String(100), nullable=False)
       price = db.Column(db.Float, nullable=False)
       description = db.Column(db.Text, nullable=True)
       category = db.Column(db.String(50), nullable=False)
       image = db.Column(db.String(200), nullable=True)

       def to_dict(self):
           return {
               'id': self.id,
               'name': self.name,
               'price': self.price,
               'description': self.description,
               'category': self.category,
               'image': self.image or 'https://placehold.co/300x200'
           }
   