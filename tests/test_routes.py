import pytest


def product_data(**changes):
    product = {
        "name": "Hammer", "description": "Claw hammer", "price": "34.95",
        "available": True, "category": "TOOLS",
    }
    product.update(changes)
    return product


def create(client, **changes):
    response = client.post("/products", json=product_data(**changes))
    assert response.status_code == 201
    return response.get_json()


def test_index_and_health(client):
    assert b"Product Catalog Administration" in client.get("/").data
    assert client.get("/health").get_json() == {"status": 200, "message": "OK"}


def test_read_a_product(client):
    created = create(client)
    response = client.get(f"/products/{created['id']}")
    assert response.get_json()["name"] == "Hammer"


def test_update_a_product(client):
    created = create(client)
    updated = client.put(
        f"/products/{created['id']}", json=product_data(name="Mallet", available=False)
    ).get_json()
    assert updated["name"] == "Mallet"


def test_delete_a_product(client):
    created = create(client)
    assert client.delete(f"/products/{created['id']}").status_code == 204
    assert client.get(f"/products/{created['id']}").status_code == 404


def test_list_all_products(client):
    create(client, name="Hat", category="CLOTHS")
    create(client, name="Hat", category="FOOD", available=False)
    assert len(client.get("/products").get_json()) == 2


def test_list_by_name(client):
    create(client, name="Hat", category="CLOTHS")
    create(client, name="Saw", category="TOOLS")
    assert len(client.get("/products?name=Hat").get_json()) == 1


def test_list_by_availability(client):
    create(client, name="Hat", category="CLOTHS")
    create(client, name="Saw", category="FOOD", available=False)
    assert client.get("/products?available=false").get_json()[0]["available"] is False


def test_list_by_category(client):
    create(client, name="Hat", category="CLOTHS")
    create(client, name="Saw", category="FOOD", available=False)
    assert client.get("/products?category=CLOTHS").get_json()[0]["category"] == "CLOTHS"


@pytest.mark.parametrize("method,url,kwargs,status", [
    ("post", "/products", {"data": "{}"}, 415),
    ("put", "/products/99", {"data": "{}"}, 415),
    ("post", "/products", {"json": {"name": "only"}}, 400),
    ("get", "/products?available=maybe", {}, 400),
    ("get", "/products?category=bad", {}, 400),
    ("put", "/products/99", {"json": product_data()}, 404),
    ("delete", "/products/99", {}, 404),
])
def test_errors(client, method, url, kwargs, status):
    assert getattr(client, method)(url, **kwargs).status_code == status
