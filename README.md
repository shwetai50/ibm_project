# Product Catalog Service

A Flask REST microservice and small administrative UI for managing an eCommerce product catalog. It implements create, read, update, delete, list, and filters by `name`, `available`, and `category`.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Open http://127.0.0.1:5000. The default database is `products.db`; override it with `SQLALCHEMY_DATABASE_URI` if required.

## Quality checks

```powershell
pytest
behave
```

The BDD suite assumes the service is running and a Selenium-compatible browser driver is available.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/products` | Create a product |
| GET | `/products` | List, optionally `?name=`, `?available=`, `?category=` |
| GET | `/products/{id}` | Read one product |
| PUT | `/products/{id}` | Update one product |
| DELETE | `/products/{id}` | Delete one product |
