# Installation
install:
	pip install -r requirements.txt

# Tests
test:
	pytest

test-unit:
	pytest -m unit

test-integration:
	pytest -m integration

# Couverture
coverage:
	pytest --cov=src/task_manager --cov-report=html --cov-report=term-missing

# Nettoyage
clean:
	rm -rf htmlcov/ .coverage .pytest_cache/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

# Qualité
lint:
	flake8 src/ tests/

# Séquence complète
all: clean install test coverage lint

.PHONY: install test test-unit test-integration coverage clean lint all 