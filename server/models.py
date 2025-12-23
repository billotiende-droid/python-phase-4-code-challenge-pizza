from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    # Relationship to RestaurantPizza
    restaurant_pizzas =relationship("RestaurantPizza", back_populates="restaurant", cascade="all, delete-orphan")

    #Association to proxy to access pizza directly
    pizzas = association_proxy("restaurant_pizzas", "pizza")

    # add serialization rules
    serialize_rules = ("-restaurant_pizzas.restaurant",) #avoid recurssion

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)

    # add relationship
    restaurant_pizzas = relationship ("RestaurantPizza", back_populates="pizza", cascade="all, delete-orphan")

    # Association proxy to access restaurant directly
    restaurants = association_proxy ("restaurant_pizzas", "restaurant")

    # add serialization rules
    serialize_rules = ("-restaurant_pizzas.restaurant",) # avoid recurssion

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    #Foreign Keys
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"), nullable=False)
    # add relationships
    restaurant = relationship("Restaurant", back_populates="restaurant_pizzas")
    pizza = relationship("Pizza", back_populates="restaurant_pizzas")
    # add serialization rules
    serialize_rules = ("-restaurant.restaurant_pizzas", "-pizza.restaurant_pizzas")
    # add validation
    @validates("price")
    def validate_price(self, key, value):
        if value < 1:
            raise ValueError("Price must be greater than or equal to 1$")
        elif value > 30:
            raise ValueError("Price can't be greater than 30")
        return value

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
