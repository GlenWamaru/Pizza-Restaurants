from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError

# Initialize SQLAlchemy
db = SQLAlchemy()

# Define the Restaurant model
class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    
    # Relationship with RestaurantPizza
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Restaurant {self.id}: {self.name}>"
    
    # Validate name length and uniqueness
    @validates('name')
    def validate_name(self, key, value):
        assert len(value) <= 50, "Name must be less than 50 characters"
        return value

# Define the Pizza model
class Pizza(db.Model):
    __tablename__ = 'pizzas'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)
    
    # Relationship with RestaurantPizza
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Pizza {self.id}: {self.name}>"

# Define the RestaurantPizza model (join table)
class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'
    
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    
    # Relationships
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')
    
    def __repr__(self):
        return f"<RestaurantPizza {self.id}: Restaurant {self.restaurant_id}, Pizza {self.pizza_id}>"
    
    # Validate price range
    @validates('price')
    def validate_price(self, key, value):
        assert 1 <= value <= 30, "Price must be between 1 and 30"
        return value
