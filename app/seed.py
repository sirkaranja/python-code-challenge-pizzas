#!/usr/bin/env python3
from faker import Faker
from random import choice as rc
from models import db, Restaurant, Pizza, Restaurant_pizza

# Create an instance of the Faker class
fake = Faker()

def seed_data(num_restaurants, num_pizzas, num_restaurant_pizzas):
    # Seed Restaurants
    for _ in range(num_restaurants):
        name = fake.company()
        address = fake.address()
        restaurant = Restaurant(name=name, address=address)
        db.session.add(restaurant)

    # Seed Pizzas
    for _ in range(num_pizzas):
        name = fake.word()
        ingredients = fake.words(nb=3)
        pizza = Pizza(name=name, ingredients=ingredients)
        db.session.add(pizza)

    # Seed Restaurant_pizzas
    restaurant_ids = [restaurant.id for restaurant in Restaurant.query.all()]
    pizza_ids = [pizza.id for pizza in Pizza.query.all()]
    for _ in range(num_restaurant_pizzas):
        price = fake.random_int(min=5, max=20)
        restaurant_id = fake.random_element(elements=restaurant_ids)
        pizza_id = fake.random_element(elements=pizza_ids)
        restaurant_pizza = Restaurant_pizza(price=price, restaurant_id=restaurant_id, pizza_id=pizza_id)
        db.session.add(restaurant_pizza)

    db.session.commit()


seed_data(num_restaurants=10, num_pizzas=20, num_restaurant_pizzas=50)
