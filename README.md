# Pizza Restaurants API
# Overview

A Flask REST API for managing pizza restaurants and menus.
Supports listing restaurants, adding pizzas to restaurants with a price, deleting restaurants, and listing all pizzas.

# Models

Restaurant: id, name, address

restaurant_pizzas → relationship to RestaurantPizza

pizzas → access pizzas via association proxy

Pizza: id, name, ingredients

restaurant_pizzas → relationship to RestaurantPizza

restaurants → access restaurants via association proxy

RestaurantPizza: id, price, restaurant_id, pizza_id

Validates price between 1 and 30

# Relationships to Restaurant and Pizza

# API Endpoints
# Method	Route	Description
GET	/restaurants	List all restaurants
GET	/restaurants/<id>	Show a restaurant with pizzas
DELETE	/restaurants/<id>	Delete a restaurant
GET	/pizzas	List all pizzas
POST	/restaurant_pizzas	Add pizza to restaurant with price
Setup
cd server
pipenv shell
pip install -r requirements.txt
export FLASK_APP=app.py
flask db init
flask db migrate 
flask db upgrade
python seed.py      
python app.py        # runs server at http://127.0.0.1:5555

# Notes

RestaurantPizza.price must be between 1–30

Uses SQLAlchemy, association proxies, and sqlalchemy-serializer for relationships and JSON output