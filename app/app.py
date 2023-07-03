

from flask import Flask, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


from models import db, Restaurant, Restaurant_pizza, Pizza
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''


if __name__ == '__main__':
    app.run(port=5555)
