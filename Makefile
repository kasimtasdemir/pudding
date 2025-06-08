.PHONY: format lint typecheck test fix check all clean install dev

# Development setup
install:
	uv pip install -e .

dev:
	uv pip install -e ".[dev]"

# Code formatting
format:
	uv run ruff format .

# Linting (without fixing)
lint:
	uv run ruff check .

# Type checking
typecheck:
	uv run mypy src/pudding/

# Auto-fix linting issues
fix:
	uv run ruff check --fix .
	uv run ruff format .

# Run tests
test:
	uv run pytest

# Quick pre-commit check (fast feedback)
check: lint typecheck

# Full CI check (what CI runs)
ci: check test

# Complete development cycle
all: fix typecheck test

# Clean up generated files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

# Help command
help:
	@echo "Available commands:"
	@echo "  dev       - Install development dependencies"
	@echo "  format    - Format code with ruff"
	@echo "  lint      - Check code with ruff (no fixes)"
	@echo "  typecheck - Run mypy type checking"
	@echo "  fix       - Auto-fix linting issues and format"
	@echo "  test      - Run pytest"
	@echo "  check     - Quick check (lint + typecheck)"
	@echo "  ci        - Full CI check (check + test)"
	@echo "  all       - Complete cycle (fix + typecheck + test)"
	@echo "  clean     - Remove generated files"