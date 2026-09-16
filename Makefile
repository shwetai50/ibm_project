.PHONY: test lint bdd run

test:
	python -m pytest

lint:
	python -m ruff check service tests

bdd:
	python -m behave

run:
	python run.py
