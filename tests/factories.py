"""Factory for fake, unsaved product instances used by tests."""
from decimal import Decimal

from service.models import Category, Product


class ProductFactory:
    """Create valid fake products without requiring a database session."""

    _sequence = 0

    def __new__(cls, **changes):
        cls._sequence += 1
        number = cls._sequence
        values = {
            "name": f"Test Product {number}",
            "description": f"Generated product number {number}",
            "price": Decimal("9.99"),
            "available": True,
            "category": Category.UNKNOWN,
        }
        values.update(changes)
        return Product(**values)
