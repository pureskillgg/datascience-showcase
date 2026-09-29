all: lint test check

format:
	@uv run black .

lint:
	@uv run pylint ./pureskillgg_datascience_showcase ./scripts ./tests ./templates/gallery-item/make.py
	@uv run black --check .

test:
	@uv run pytest --cov=./pureskillgg_datascience_showcase

check:
	@uv run python scripts/check_repo.py --all
	@uv run python scripts/build_gallery.py --check

gallery:
	@uv run python scripts/build_gallery.py

style-guide:
	@uv run python scripts/render_style_guide.py

hooks:
	@uv run pre-commit install

watch:
	@uv run ptw

notebook:
	@uv run jupyter notebook

.PHONY: all check format gallery hooks lint notebook style-guide test watch
