.PHONY: clean install migrate  lint test format

default: clean install reset frontend

clean:
	find . -name '*.pyc' -exec rm -rf {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.egg-info' -exec rm -rf {} +

install:
	poetry install

migrate:
	sandbox/manage.py migrate

test:
	pytest --reuse-db

cov:
	coverage run -pm pytest --reuse-db
	coverage html

format:
	ruff check src tests sandbox --fix
	ruff format src tests sandbox
