

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


from models import db, Restaurant, Restaurant_pizza, Pizza
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurant_list = []

    for restaurant in Restaurant.query.all():
        restaurant_data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address
        }
        restaurant_list.append(restaurant_data)

    response=make_response(
        jsonify(restaurant_list),
        201
    )

    return response



@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)

    if restaurant is None:
        return jsonify({'error': 'Restaurant not found'}), 404

    pizzas = []
    for restaurant_pizza in restaurant.pizzas:
        pizza = restaurant_pizza.pizza
        pizza_data = {
            'id': pizza.id,
            'name': pizza.name,
            'ingredients': pizza.ingredients
        }
        pizzas.append(pizza_data)

    restaurant_data = {
        'id': restaurant.id,
        'name': restaurant.name,
        'address': restaurant.address,
        'pizzas': pizzas
    }

    return jsonify(restaurant_data)


@app.route('/restaurants', methods=['POST'])
def create_restaurant():
    data = request.get_json()

    name = data.get('name')
    address = data.get('address')

    if not name or not address:
        return jsonify({'errors': ['Missing required data']}), 400

    restaurant = Restaurant(name=name, address=address)
    db.session.add(restaurant)
    db.session.commit()

    restaurant_data = {
        'id': restaurant.id,
        'name': restaurant.name,
        'address': restaurant.address
    }
    response=make_response(
        jsonify(restaurant_data),
        201
    )

    return response

@app.route('/restaurants/<int:id>', methods=['PUT'])
def update_restaurant(id):
    data = request.get_json()

    name = data.get('name')
    address = data.get('address')

    restaurant = Restaurant.query.get(id)

    if restaurant is None:
        return jsonify({'error': 'Restaurant not found'}), 404

    if name is not None:
        restaurant.name = name

    if address is not None:
        restaurant.address = address

    db.session.commit()

    response= make_response(
        jsonify({'message': 'Restaurant updated'}),200
    )
    return response

    


@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)

    if restaurant is None:
        return jsonify({'error': 'Restaurant not found'}), 404

    db.session.delete(restaurant)
    db.session.commit()

    return '', 204


@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    pizza_list = []

    for pizza in pizzas:
        pizza_data = {
            'id': pizza.id,
            'name': pizza.name,
            'ingredients': pizza.ingredients
        }
        pizza_list.append(pizza_data)

    return jsonify(pizza_list), 200
    

if __name__ == '__main__':
    app.run(port=5555)
