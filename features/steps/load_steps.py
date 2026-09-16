"""Behave setup step for loading deterministic product data."""
import requests
from behave import given


def endpoint(context, suffix=""):
    return f"{context.base_url}/products{suffix}"


@given("the following products")
def load_products(context):
    for product in requests.get(endpoint(context)).json():
        assert requests.delete(endpoint(context, f"/{product['id']}")).status_code == 204
    for row in context.table:
        data = dict(row.items())
        data["available"] = data["available"] == "True"
        assert requests.post(endpoint(context), json=data).status_code == 201
