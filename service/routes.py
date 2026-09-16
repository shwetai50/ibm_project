"""HTTP API endpoints for the catalog."""
from flask import Blueprint, abort, current_app, jsonify, request

from service.models import Category, DataValidationError, Product

api = Blueprint("api", __name__)


@api.get("/")
def index():
    return current_app.send_static_file("index.html")


@api.get("/health")
def healthcheck():
    return jsonify(status=200, message="OK")


def product_or_404(product_id):
    product = Product.find(product_id)
    if product is None:
        abort(404, description=f"Product with id {product_id} was not found")
    return product


@api.errorhandler(DataValidationError)
def validation_error(error):
    return jsonify(error=str(error)), 400


@api.post("/products")
def create_product():
    if not request.is_json:
        abort(415, description="Content-Type must be application/json")
    product = Product().deserialize(request.get_json())
    product.create()
    response = jsonify(product.serialize())
    response.status_code = 201
    response.headers["Location"] = f"/products/{product.id}"
    return response


@api.get("/products")
def list_products():
    name = request.args.get("name")
    available = request.args.get("available")
    category = request.args.get("category")
    if name is not None:
        products = Product.find_by_name(name)
    elif category is not None:
        try:
            products = Product.find_by_category(Category[category.upper()])
        except KeyError:
            abort(400, description="category is invalid")
    elif available is not None:
        if available.lower() not in ("true", "false"):
            abort(400, description="available must be true or false")
        products = Product.find_by_availability(available.lower() == "true")
    else:
        products = Product.all()
    return jsonify([product.serialize() for product in products])


@api.get("/products/<int:product_id>")
def get_product(product_id):
    return jsonify(product_or_404(product_id).serialize())


@api.put("/products/<int:product_id>")
def update_product(product_id):
    if not request.is_json:
        abort(415, description="Content-Type must be application/json")
    product = product_or_404(product_id)
    product.deserialize(request.get_json())
    product.update()
    return jsonify(product.serialize())


@api.delete("/products/<int:product_id>")
def delete_product(product_id):
    product_or_404(product_id).delete()
    return "", 204
