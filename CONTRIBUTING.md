# Contributing to Chicago Crime Intelligence Hub

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Commit Messages](#commit-messages)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you are expected to uphold this code.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your changes
4. Make your changes
5. Submit a pull request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/your-username/crime-hub.git
cd crime-hub

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Pull Request Process

1. **Update the README.md** with details of changes to the interface if applicable
2. **Update the AGENTS.md** if you add new commands or change workflows
3. **Add tests** for any new functionality
4. **Ensure all tests pass** before submitting
5. **Update the version number** in `pyproject.toml` if appropriate
6. **Submit your pull request**

### Pull Request Checklist

- [ ] Code follows the project's style guidelines
- [ ] Tests pass locally (`make test`)
- [ ] Linting passes (`make lint`)
- [ ] Documentation is updated if needed
- [ ] Commit messages are clear and descriptive

## Coding Standards

### Python Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) guidelines
- Use [Black](https://github.com/psf/black) for code formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Maximum line length: 88 characters

### Code Organization

- Keep functions focused and small
- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Follow the existing project structure

### Example

```python
def calculate_arrest_rate(total: int, arrests: int) -> float:
    """
    Calculate arrest rate as a percentage.
    
    Args:
        total: Total number of incidents
        arrests: Number of arrests made
    
    Returns:
        Arrest rate as a percentage (0-100)
    """
    if total == 0:
        return 0.0
    return (arrests / total) * 100
```

## Commit Messages

Use clear, descriptive commit messages:

```
type(scope): brief description

Longer description if needed to explain the change.

Fixes #123
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

## Running Tests

```bash
# Run all tests
make test

# Run with coverage
python -m pytest tests/ -v --cov=. --cov-report=term-missing

# Run specific test file
python -m pytest tests/test_project.py -v
```

## Project Structure

See [README.md](README.md) for the complete project structure and documentation.

## Questions or Issues?

- Open an issue on the [GitHub Issues page](https://github.com/therealshammz/crime-hub/issues)
- Check existing issues before creating new ones