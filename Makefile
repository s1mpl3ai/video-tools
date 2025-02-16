# Variables
VENV_DIR := myenv
PYTHON := $(shell pyenv which python)  # Use pyenv-managed Python
PIP := $(VENV_DIR)/bin/pip
FLASK := $(VENV_DIR)/bin/flask
PYTHONVENV := $(VENV_DIR)/bin/python
# Default target
.PHONY: help
help:
	@echo "Usage:"
	@echo "  make install     Set up virtual environment and install dependencies"
	@echo "  make db_init     Initialize the SQLite database"
	@echo "  make run         Run the Flask development server"
	@echo "  make test        Run tests with coverage"
	@echo "  make clean       Remove temporary files and caches"

# Set up virtual environment and install dependencies
.PHONY: install
install:
	$(PYTHON) -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Initialize the SQLite database
.PHONY: db_init
db_init: install
	FLASK_APP=app:create_app $(FLASK) db init
	FLASK_APP=app:create_app $(FLASK) db migrate -m "Initial migration."
	FLASK_APP=app:create_app $(FLASK) db upgrade

# Run the Flask development server
.PHONY: run
run: install
	$(FLASK) run

# Run tests with coverage
.PHONY: test
test: install
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +
	$(PYTHONVENV) -m coverage run -m unittest discover -s app/tests -p "test_*.py"
	$(PYTHONVENV) -m coverage report -m -i
	$(PYTHONVENV) -m coverage html  

# Clean temporary files and caches
.PHONY: clean
clean:
	rm -rf $(VENV_DIR)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf migrations
	rm -f app/app.db
	rm -rf file_object_storage
	mkdir file_object_storage
	rm -rf .coverage htmlcov/