from app import app, db
from models import Restaurant, Pizza, RestaurantPizza

def seed_data():
    # Create sample restaurants
    restaurant1 = Restaurant(name="Pizza Paradise", address="123 Main St")
    restaurant2 = Restaurant(name="The Pizza Place", address="456 Elm St")
    
    # Create sample pizzas
    pizza1 = Pizza(name="Margherita", ingredients="Tomato sauce, mozzarella, basil")
    pizza2 = Pizza(name="Pepperoni", ingredients="Tomato sauce, mozzarella, pepperoni")
    
    # Create sample restaurant-pizza relationships with prices
    rp1 = RestaurantPizza(restaurant=restaurant1, pizza=pizza1, price=9.99)
    rp2 = RestaurantPizza(restaurant=restaurant1, pizza=pizza2, price=11.99)
    rp3 = RestaurantPizza(restaurant=restaurant2, pizza=pizza1, price=10.99)
    rp4 = RestaurantPizza(restaurant=restaurant2, pizza=pizza2, price=12.99)
    
    # Add all instances to the database session and commit
    db.session.add_all([restaurant1, restaurant2, pizza1, pizza2, rp1, rp2, rp3, rp4])
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
        seed_data()  # Call the function to seed data
