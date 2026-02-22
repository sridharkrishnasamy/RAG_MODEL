.PHONY: help install dev run clean setup test lint format

help:
	@echo "PDF Compliance Checker - Makefile Commands"
	@echo ""
	@echo "make install    - Install dependencies with uv"
	@echo "make dev        - Install with dev dependencies"
	@echo "make setup      - Initialize project"
	@echo "make run        - Start Streamlit app"
	@echo "make clean      - Remove cache and build files"
	@echo "make lint       - Run linters"
	@echo "make format     - Format code with black"
	@echo "make test       - Run tests"

install:
	uv pip install -e .

dev:
	uv pip install -e ".[dev]"

setup:
	python setup.py

run:
	streamlit run app.py

clean:
	rm -rf __pycache__ .pytest_cache .coverage htmlcov build dist
	rm -rf data/vector_store/*.pkl
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

lint:
	pylint *.py --disable=C0111,R0903

format:
	black *.py

test:
	pytest -v

requirements:
	pip freeze > requirements.txt

.env:
	cp .env.example .env
	@echo "Created .env file. Please add your GOOGLE_API_KEY"

venv:
	python3 -m venv venv

all: venv install setup .env run
