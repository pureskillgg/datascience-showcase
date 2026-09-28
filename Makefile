all: lint test check

format:
	@uv run black .

lint:
	@uv run pylint ./pureskillgg_datascience_showcase ./scripts ./tests
	@uv run black --check .

test:
	@uv run pytest --cov=./pureskillgg_datascience_showcase

check:
	@uv run python scripts/check_repo.py --all

hooks:
	@uv run pre-commit install

watch:
	@uv run ptw

notebook:
	@uv run jupyter notebook

.PHONY: all check format hooks lint notebook test watch
