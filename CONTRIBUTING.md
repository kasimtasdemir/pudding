# Contributing to Pudding

We love your input! We want to make contributing to Pudding as easy and transparent as possible.

## Development Setup

We use `uv` for dependency management:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repo
git clone https://github.com/yourusername/pudding.git
cd pudding

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

## Development Workflow

1. Fork the repo and create your branch from `development`
2. Make your changes and test incrementally  
```uv run pytest tests/test_specific.py::test_one_thing```
1. Add tests for any new functionality
2. Ensure tests pass: `uv run pytest`
3. Format & lint code:  `uv run ruff format . && uv run ruff check .`
4. Commit  `git add .
git commit -m "feat: add new capability" `
1. Submit a pull request!
```
# 8. Before release
# Update CHANGELOG.md under [Unreleased]
# Then bump version
bump-my-version patch
git push --tags
```

## Version Management

We use [bump-my-version](https://github.com/callowayproject/bump-my-version) for version management.

### Setup (first time only)

```bash
# The .bumpversion.cfg file should already exist in the repo
```

### Bumping Versions

Before releasing a new version:

1. Ensure all changes are committed
2. Update CHANGELOG.md (move items from "Unreleased" to the new version section)
3. Run the appropriate bump command:

```bash
# For bug fixes (0.1.0 → 0.1.1)
bump-my-version patch

# For new features (0.1.1 → 0.2.0)
bump-my-version minor

# For breaking changes (0.2.0 → 1.0.0)
bump-my-version major
```

This will:
- Update the version in `src/pudding/__init__.py`
- Create a git commit with message "chore: bump version X.X.X → Y.Y.Y"
- Create a git tag "vY.Y.Y"

4. Push the commit and tag:
```bash
git push
git push --tags
```

### Version Guidelines

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes (incompatible API changes)
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

### Pre-release Versions

For alpha/beta releases:
```bash
# Create alpha version (0.2.0 → 0.2.0a1)
bump-my-version pre_release --pre alpha

# Create beta version (0.2.0a1 → 0.2.0b1)
bump-my-version pre_release --pre beta

# Move to release candidate (0.2.0b1 → 0.2.0rc1)
bump-my-version pre_release --pre rc

# Final release (0.2.0rc1 → 0.2.0)
bump-my-version pre_release
```


## Code Style

We use `ruff` for both formatting and linting. It's configured to match Black's style.

Run before committing:
```bash
# Format code
uv run ruff format .

# Check for linting issues
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check --fix .
```
- Type hints where practical

## Testing

Run tests with:
```bash
uv run pytest
```

## Documentation

Update documentation if you're changing functionality. Docs live in the `docs/` folder.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
