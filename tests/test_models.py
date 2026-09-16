from decimal import Decimal

import pytest

from service import create_app
from service.models import Category, DataValidationError, Product, db
from tests.factories import ProductFactory


@pytest.fixture()
def app(tmp_path):
    app = create_app(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'model.db'}"}
    )
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


def data(**changes):
    product = {
        "name": "Hammer", "description": "Claw hammer", "price": "34.95",
        "available": True, "category": "TOOLS",
    }
    product.update(changes)
    return product


def test_create_a_product(app):
    with app.app_context():
        product = ProductFactory(name="Hammer", description="Claw hammer", price=Decimal("34.95"))
        product.create()
        assert product.id is not None


def test_read_a_product(app):
    with app.app_context():
        product = Product().deserialize(data())
        product.create()
        assert Product.find(product.id).serialize() == {"id": product.id, **data()}


def test_update_a_product(app):
    with app.app_context():
        product = Product().deserialize(data())
        product.create()
        product.name = "Heavy hammer"
        product.update()
        assert Product.all()[0].name == "Heavy hammer"


def test_delete_a_product(app):
    with app.app_context():
        product = Product().deserialize(data())
        product.create()
        product.delete()
        assert Product.all() == []


def test_list_all_products(app):
    with app.app_context():
        Product().deserialize(data()).create()
        Product().deserialize(data(name="Saw")).create()
        assert [product.name for product in Product.all()] == ["Hammer", "Saw"]


def test_find_by_name(app):
    with app.app_context():
        Product().deserialize(data()).create()
        Product().deserialize(data(name="Saw")).create()
        assert [product.name for product in Product.find_by_name("Saw")] == ["Saw"]


def test_find_by_category(app):
    with app.app_context():
        Product().deserialize(data()).create()
        Product().deserialize(data(name="Hat", category="CLOTHS")).create()
        assert [product.name for product in Product.find_by_category(Category.CLOTHS)] == ["Hat"]


def test_find_by_availability(app):
    with app.app_context():
        Product().deserialize(data()).create()
        Product().deserialize(data(name="Saw", available=False)).create()
        assert [product.name for product in Product.find_by_availability(False)] == ["Saw"]


@pytest.mark.parametrize(
    "bad",
    [
        None, [], {"name": "Hammer"}, data(name=""), data(description=3),
        data(available="true"), data(price="nope"), data(price="-1"), data(category="OTHER"),
    ],
)
def test_deserialize_rejects_invalid_data(bad):
    with pytest.raises(DataValidationError):
        Product().deserialize(bad)


def test_update_without_id_and_category_values():
    with pytest.raises(DataValidationError, match="empty ID"):
        Product().update()
    assert Category.TOOLS.name == "TOOLS"
    assert Decimal("34.95") == Product().deserialize(data()).price
