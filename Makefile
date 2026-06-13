all: lint test

build:
	@rm -rf dist
	@uv build

format:
	@uv run black .

lint:
	@uv run pylint ./pureskillgg_datascience_showcase
	@uv run black --check .

publish:
	@uv run twine upload --skip-existing dist/*

test:
	@uv run pytest --cov=./pureskillgg_datascience_showcase

watch:
	@uv run ptw

notebook:
	@uv run jupyter notebook notebooks

.PHONY: build docs test
