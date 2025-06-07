# Pudding Developer Guide
Welcome! This guide will help you contribute to Pudding following best practices for open source projects.

## 🎯 Contributing to Pudding

### 📋 Before You Code

**Always create a GitHub issue first!** This ensures:
- Clear communication about what you're working on
- Issue numbers for branch naming
- Opportunity for discussion before implementation
- Proper tracking of project progress

### 🌿 Git Workflow

#### Branch Naming Convention
```
type/issue-number-short-description
```

**Branch Types:**
- `feature/` - New functionality
- `bugfix/` - Bug fixes (non-critical)
- `hotfix/` - Critical production fixes
- `docs/` - Documentation only
- `refactor/` - Code restructuring
- `test/` - Test additions/modifications
- `chore/` - Maintenance (deps, configs, etc.)

**Examples:**
```bash
feature/42-add-data-envelope
bugfix/13-fix-null-validation
docs/7-update-api-reference
```

#### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation only
- `style` - Formatting, missing semicolons, etc.
- `refactor` - Code change that neither fixes a bug nor adds a feature
- `test` - Adding missing tests
- `perf` - Performance improvement
- `build` - Changes to build system or dependencies
- `ci` - CI configuration files and scripts
- `chore` - Other changes that don't modify src or test files
- `revert` - Reverts a previous commit

**Examples:**
```bash
feat(core): add BaseComponent framework
fix(registry): resolve component compatibility checking bug
docs: update installation instructions
test: add integration tests for BaseComponent
```

### 🔄 Pull Request Process

1. **Branch from `main`** (or `develop` if using GitFlow)
2. **Make atomic commits** - Each commit should represent one logical change
3. **Write descriptive PR titles** - Same format as commit messages
4. **Use PR template** - Fill out all sections
5. **Link issues** - Use keywords like `Closes #42` or `Fixes #13`
6. **Request reviews** - At least one approval required
7. **Keep updated** - Rebase on main if needed


### 📊 Issue Management

#### Issue Labels
- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `question` - Further information requested
- `wontfix` - This will not be worked on
- `duplicate` - This issue already exists

#### Issue Templates
Use provided templates for:
- 🐛 Bug Report
- ✨ Feature Request
- 📚 Documentation Update
- ❓ Question

### 🏗️ Code Standards

#### Python Style
- Follow [PEP 8](https://pep8.org/)
- Use type hints where applicable
- Maximum line length: 88 characters (Black default)
- Docstrings for all public methods

#### Testing
- Write tests for new features
- Maintain or increase coverage
- Use pytest for testing
- Test files mirror source structure

### 🚀 Release Process

1. Create release branch: `release/vX.Y.Z`
2. Update version numbers
3. Update CHANGELOG.md
4. Create PR to main
5. Tag release after merge: `vX.Y.Z`
6. GitHub automatically creates release

## Tools
### VS Code Settings

Install Ruff extension.
```json
{
    "python.linting.enabled": true,
    "[python]": {
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll": "explicit",
            "source.organizeImports": "explicit"
        },
        "editor.defaultFormatter": "charliermarsh.ruff"
    },
    "ruff.path": [".venv/bin/ruff"],
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false
}
```

## Architecture Overview

TODO: Add architecture details

## Component Development

TODO: Add component development guide

## Best Practices

TODO: Add best practices

## Debugging Tips

TODO: Add debugging tips

## Performance Considerations

TODO: Add performance guide
