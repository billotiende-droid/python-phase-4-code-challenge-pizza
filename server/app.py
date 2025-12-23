#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route("/restaurants", methods=['GET'] )
def get_restaurants():

    restaurants = []

    for restaurant in Restaurant.query.all():
        # dictionar for JSON output
        restaurant_dict ={
            "address":restaurant.address,
            "id":restaurant.id,
            "name":restaurant.name
        }
        restaurants.append(restaurant_dict) 

    return make_response(restaurants, 200)

@app.route("/restaurants/<int:id>", methods =['GET'])
def get_restaurant_by_id(id):

    restaurant = Restaurant.query.filter(Restaurant.id ==id).first()
    #error message for invalid ids
    if not restaurant:
        return make_response({"error":"Restaurant not available"}, 404)
    
    restaurant_dict ={
        "address":restaurant.address,
        "id":restaurant.id,
        "name":restaurant.name,
        "restaurant_pizzas":[]   #empty list which will be appended when using a for loop
    }

    for restaurant_pizza in restaurant.restaurant_pizzas:
        restaurant_pizza_dict ={
            "id":restaurant_pizza.id,
            "pizza":{
                "id":restaurant_pizza.id,
                "name":restaurant_pizza.name,
                "ingredients":restaurant_pizza.ingredients
            },
            "pizza_id":restaurant_pizza.pizza_id,
            "price":restaurant_pizza.price,
            "restaurant_id":restaurant_pizza.restaurant_id
        }
        #appends  the dictionary under the for loop to the empty list
        restaurant_dict["restaurant_pizzas"].append(restaurant_pizza_dict)

        return make_response(restaurant_dict, 200)
    
    @app.route("/restaurants/<int:id>", methods=['DELETE'])
    def delete_restaurant_by_id(id):

        restaurant =Restaurant.query.filter(Restaurant.id ==id).first()

        if not restaurant:
            return make_response({"error":"Restaurant not found"}, 404)

        db.session.delete(restaurant)
        db.session.commit()

        return make_response("", 204) 
     


if __name__ == "__main__":
    app.run(port=5555, debug=True)
