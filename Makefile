all: lint test

build:
	@rm -rf dist
	@poetry build

format:
	@poetry run black .

lint:
	@poetry run pylint ./pureskillgg_datascience_showcase
	@poetry run black --check .

publish:
	@poetry run twine upload --skip-existing dist/*

test:
	@poetry run pytest --cov=./pureskillgg_datascience_showcase

watch:
	@poetry run ptw

notebook:
	@poetry run jupyter notebook notebooks

.PHONY: build docs test
