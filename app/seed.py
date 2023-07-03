from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from faker import Faker

from models import db, Restaurant, Pizza, Restaurant_pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

fake = Faker()

# Import the necessary SQLAlchemy models from your models.py file

def seed_data():
    with app.app_context():
        db.create_all()

        # Create some restaurants
        for _ in range(5):
            restaurant = Restaurant(name=fake.company(), address=fake.address())
            db.session.add(restaurant)

        # Create some pizzas
        for _ in range(10):
            pizza = Pizza(name=fake.word(), ingredients=fake.text())
            db.session.add(pizza)

        # Add objects to the session
        db.session.commit()

        # Add relationships between restaurants and pizzas
        restaurants = Restaurant.query.all()
        pizzas = Pizza.query.all()

        for restaurant in restaurants:
            # Randomly select a few pizzas to associate with each restaurant
            pizzas_to_associate = fake.random_elements(elements=pizzas, length=fake.random_int(min=1, max=5), unique=True)

            for pizza in pizzas_to_associate:
                # Create a RestaurantPizza object to represent the relationship
                restaurant_pizza = Restaurant_pizza(price=fake.random_int(min=5, max=20), restaurant=restaurant, pizza=pizza)
                db.session.add(restaurant_pizza)

        # Commit the changes to the database
        db.session.commit()

# Call the seed_data function to populate the tables
seed_data()

if __name__ == '__main__':
    app.run()