"""Step definitions that exercise the product catalog through its HTTP UI/API."""
import requests
from behave import then, when


def endpoint(context, suffix=""):
    return f"{context.base_url}/products{suffix}"


@when('I create a product named "{name}"')
def create_product(context, name):
    payload = {
        "name": name, "description": "Created by BDD", "price": "9.99",
        "available": True, "category": "TOOLS",
    }
    context.response = requests.post(endpoint(context), json=payload)


@when('I retrieve the product named "{name}"')
def retrieve_product(context, name):
    context.response = requests.get(endpoint(context, f"?name={name}"))
    context.product = context.response.json()[0]


@then('the retrieved product is named "{name}"')
def retrieved_name(context, name):
    assert context.product["name"] == name


@when('I rename the product "{old}" to "{new}"')
def rename_product(context, old, new):
    product = requests.get(endpoint(context, f"?name={old}")).json()[0]
    product["name"] = new
    context.response = requests.put(endpoint(context, f"/{product['id']}"), json=product)


@when('I delete the product named "{name}"')
def delete_product(context, name):
    product = requests.get(endpoint(context, f"?name={name}")).json()[0]
    context.response = requests.delete(endpoint(context, f"/{product['id']}"))


@when("I list all products")
def list_all(context):
    context.response = requests.get(endpoint(context))


@when('I list products named "{name}"')
def list_by_name(context, name):
    context.response = requests.get(endpoint(context, f"?name={name}"))


@when('I list products in category "{category}"')
def list_by_category(context, category):
    context.response = requests.get(endpoint(context, f"?category={category}"))


@when('I list products with availability "{available}"')
def list_by_availability(context, available):
    context.response = requests.get(endpoint(context, f"?available={available}"))


@then('the product list contains "{name}"')
def list_contains(context, name):
    assert any(product["name"] == name for product in requests.get(endpoint(context)).json())


@then('the product list does not contain "{name}"')
def list_lacks(context, name):
    assert not any(product["name"] == name for product in requests.get(endpoint(context)).json())


@then('I receive {count:d} products')
def count_products(context, count):
    assert context.response.status_code == 200
    assert len(context.response.json()) == count
