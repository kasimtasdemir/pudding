.PHONY: format lint test clean

format:
	uv run ruff format .

lint:
	uv run ruff check .

fix:
	uv run ruff check --fix .
	uv run ruff format .

test:
	uv run pytest

all: fix test

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete