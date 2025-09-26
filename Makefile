# Amazon Review Scraper API Makefile

.PHONY: help install install-dev test run clean docker-build docker-run docker-stop format lint

# Default target
help:
	@echo "Amazon Review Scraper API - Available Commands:"
	@echo ""
	@echo "Setup:"
	@echo "  install      Install production dependencies"
	@echo "  install-dev  Install development dependencies"
	@echo "  setup        Full setup (install + playwright browsers)"
	@echo ""
	@echo "Development:"
	@echo "  run          Run the Flask API server"
	@echo "  test         Run tests"
	@echo "  format       Format code with Black"
	@echo "  lint         Run linting with flake8"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build Build Docker image"
	@echo "  docker-run   Run with Docker Compose"
	@echo "  docker-stop  Stop Docker containers"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean        Clean up temporary files"
	@echo "  help         Show this help message"

# Setup commands
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -e .[dev]

setup: install
	playwright install chromium

# Development commands
run:
	python api_server.py

test:
	python test_api.py

format:
	black .

lint:
	flake8 .

# Docker commands
docker-build:
	docker build -t amazon-review-scraper-api .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

# Maintenance
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.log" -delete
	find . -type f -name "debug_page.png" -delete
	find . -type f -name "reviews.json" -delete
