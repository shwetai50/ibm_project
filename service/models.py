"""Persistence model and validation for catalog products."""
from decimal import Decimal, InvalidOperation
from enum import Enum

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DataValidationError(ValueError):
    """Raised when supplied product data is invalid."""


class Category(Enum):
    UNKNOWN = 0
    CLOTHS = 1
    FOOD = 2
    HOUSEWARES = 3
    AUTOMOTIVE = 4
    TOOLS = 5


class Product(db.Model):
    """A product maintained by the catalog administrator."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)
    category = db.Column(db.Enum(Category), nullable=False, default=Category.UNKNOWN)

    def create(self):
        self.id = None
        db.session.add(self)
        db.session.commit()

    def update(self):
        if self.id is None:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {"id": self.id, "name": self.name, "description": self.description,
                "price": f"{self.price:.2f}", "available": self.available,
                "category": self.category.name}

    def deserialize(self, data):
        if not isinstance(data, dict):
            raise DataValidationError("Request body must be a JSON object")
        required = ("name", "description", "price", "available", "category")
        missing = [key for key in required if key not in data]
        if missing:
            raise DataValidationError(f"Missing required field: {missing[0]}")
        if not isinstance(data["name"], str) or not data["name"].strip():
            raise DataValidationError("name must be a non-empty string")
        if not isinstance(data["description"], str):
            raise DataValidationError("description must be a string")
        if not isinstance(data["available"], bool):
            raise DataValidationError("available must be a boolean")
        try:
            price = Decimal(str(data["price"]))
        except (InvalidOperation, ValueError) as error:
            raise DataValidationError("price must be numeric") from error
        if price < 0:
            raise DataValidationError("price cannot be negative")
        try:
            category = Category[str(data["category"]).upper()]
        except KeyError as error:
            raise DataValidationError("category is invalid") from error
        self.name, self.description, self.price = data["name"].strip(), data["description"], price
        self.available, self.category = data["available"], category
        return self

    @classmethod
    def find(cls, product_id):
        return db.session.get(cls, product_id)

    @classmethod
    def all(cls):
        return cls.query.order_by(cls.id).all()

    @classmethod
    def find_by_name(cls, name):
        """Return all products whose name exactly matches *name*."""
        return cls.query.filter(cls.name == name).order_by(cls.id).all()

    @classmethod
    def find_by_category(cls, category):
        """Return all products in a category."""
        return cls.query.filter(cls.category == category).order_by(cls.id).all()

    @classmethod
    def find_by_availability(cls, available):
        """Return all products with the requested availability."""
        return cls.query.filter(cls.available == available).order_by(cls.id).all()
