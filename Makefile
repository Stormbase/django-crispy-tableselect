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

lint:
	flake8 src tests

test:
	pytest --reuse-db

cov:
	pytest --reuse-db --cov=django_crispy_tableselect --cov-report=html

format:
	black src tests
	isort src tests
