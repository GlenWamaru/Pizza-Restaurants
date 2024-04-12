from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Restaurant, Pizza, RestaurantPizza
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)



# Define routes

# GET /restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    restaurants_json = [
        {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address
        } for restaurant in restaurants
    ]
    return jsonify(restaurants_json)

# GET /restaurants/:id
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        pizzas = [
            {
                "id": rp.pizza.id,
                "name": rp.pizza.name,
                "ingredients": rp.pizza.ingredients
            } for rp in restaurant.restaurant_pizzas
        ]
        return jsonify({
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "pizzas": pizzas
        }), 200
    else:
        return jsonify({"error": "Restaurant not found"}), 404

# DELETE /restaurants/:id
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    else:
        return jsonify({"error": "Restaurant not found"}), 404

# GET /pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    pizzas_json = [
        {
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        } for pizza in pizzas
    ]
    return jsonify(pizzas_json)

# POST /restaurant_pizzas
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    # Validate the required fields
    if price is None or pizza_id is None or restaurant_id is None:
        return jsonify({"errors": ["Missing required fields"]}), 400

    # Check for validation errors in the RestaurantPizza model
    if not (1 <= price <= 30):
        return jsonify({"errors": ["Price must be between 1 and 30"]}), 400

    # Check if the restaurant and pizza exist
    restaurant = Restaurant.query.get(restaurant_id)
    pizza = Pizza.query.get(pizza_id)

    if not restaurant:
        return jsonify({"errors": ["Restaurant not found"]}), 404
    if not pizza:
        return jsonify({"errors": ["Pizza not found"]}), 404

    # Create a new RestaurantPizza
    new_restaurant_pizza = RestaurantPizza(
        price=price,
        pizza_id=pizza_id,
        restaurant_id=restaurant_id
    )
    db.session.add(new_restaurant_pizza)
    db.session.commit()

    # Return the data related to the Pizza
    pizza_data = {
        "id": pizza.id,
        "name": pizza.name,
        "ingredients": pizza.ingredients
    }

    return jsonify(pizza_data), 201

# Run the application
if __name__ == '__main__':
    app.run(port=5555, debug=True)
