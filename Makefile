# ============================================================
# EditalShield - Makefile
# Automation for development and deployment
# ============================================================

.PHONY: help docker-up docker-down docker-build docker-logs \
        train generate-data db-shell pgadmin clean test

# Colors
GREEN  := \033[0;32m
YELLOW := \033[0;33m
CYAN   := \033[0;36m
RESET  := \033[0m

help:
	@echo "$(CYAN)EditalShield - Available Commands$(RESET)"
	@echo "=============================================="
	@echo ""
	@echo "$(GREEN)Docker Commands:$(RESET)"
	@echo "  make docker-up      - Start all services (DB + pgAdmin)"
	@echo "  make docker-down    - Stop all services"
	@echo "  make docker-build   - Build Docker images"
	@echo "  make docker-logs    - View container logs"
	@echo ""
	@echo "$(GREEN)Database Commands:$(RESET)"
	@echo "  make db-shell       - Open PostgreSQL shell"
	@echo "  make pgadmin        - Open pgAdmin in browser"
	@echo "  make db-reset       - Reset database with fresh data"
	@echo ""
	@echo "$(GREEN)ML Commands:$(RESET)"
	@echo "  make generate-data  - Generate synthetic training data"
	@echo "  make train          - Train Bayesian model"
	@echo "  make train-docker   - Train model inside Docker"
	@echo ""
	@echo "$(GREEN)Development:$(RESET)"
	@echo "  make install        - Install Python dependencies"
	@echo "  make test           - Run tests"
	@echo "  make clean          - Clean generated files"
	@echo ""

# ============================================================
# Docker Commands
# ============================================================

docker-up:
	@echo "$(CYAN)Starting EditalShield services...$(RESET)"
	docker-compose up -d db pgadmin
	@echo "$(GREEN)✓ Services started!$(RESET)"
	@echo "  PostgreSQL: localhost:5432"
	@echo "  pgAdmin: http://localhost:5050"

docker-down:
	@echo "$(CYAN)Stopping services...$(RESET)"
	docker-compose down
	@echo "$(GREEN)✓ Services stopped$(RESET)"

docker-build:
	@echo "$(CYAN)Building Docker images...$(RESET)"
	docker-compose build
	@echo "$(GREEN)✓ Build complete$(RESET)"

docker-logs:
	docker-compose logs -f

docker-shell:
	docker-compose exec app /bin/bash

# ============================================================
# Database Commands
# ============================================================

db-shell:
	@echo "$(CYAN)Connecting to PostgreSQL...$(RESET)"
	docker-compose exec db psql -U postgres -d editalshield

db-reset:
	@echo "$(YELLOW)Warning: This will reset all data!$(RESET)"
	docker-compose down -v
	docker-compose up -d db
	@echo "$(GREEN)✓ Database reset complete$(RESET)"

pgadmin:
	@echo "$(CYAN)Opening pgAdmin...$(RESET)"
	start http://localhost:5050 || xdg-open http://localhost:5050 || open http://localhost:5050

# ============================================================
# ML Commands
# ============================================================

generate-data:
	@echo "$(CYAN)Generating synthetic data...$(RESET)"
	python database/generate_synthetic_data.py
	@echo "$(GREEN)✓ Data generated in data/$(RESET)"

train:
	@echo "$(CYAN)Training Bayesian model...$(RESET)"
	python models/train_bayesian_model.py
	@echo "$(GREEN)✓ Model trained and saved in models/$(RESET)"

train-docker:
	@echo "$(CYAN)Training model in Docker...$(RESET)"
	docker-compose run --rm trainer
	@echo "$(GREEN)✓ Training complete$(RESET)"

# ============================================================
# Development
# ============================================================

install:
	@echo "$(CYAN)Installing dependencies...$(RESET)"
	pip install -r requirements.txt
	@echo "$(GREEN)✓ Dependencies installed$(RESET)"

test:
	@echo "$(CYAN)Running tests...$(RESET)"
	pytest tests/ -v
	@echo "$(GREEN)✓ Tests complete$(RESET)"

lint:
	@echo "$(CYAN)Running linter...$(RESET)"
	black --check src/ database/ models/
	@echo "$(GREEN)✓ Lint complete$(RESET)"

format:
	@echo "$(CYAN)Formatting code...$(RESET)"
	black src/ database/ models/
	@echo "$(GREEN)✓ Code formatted$(RESET)"

clean:
	@echo "$(CYAN)Cleaning generated files...$(RESET)"
	rm -rf __pycache__ .pytest_cache .coverage
	rm -rf data/*.json data/*.sql
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Clean complete$(RESET)"

# ============================================================
# Quick Start
# ============================================================

quickstart: docker-up generate-data
	@echo ""
	@echo "$(GREEN)============================================$(RESET)"
	@echo "$(GREEN)EditalShield is ready!$(RESET)"
	@echo "$(GREEN)============================================$(RESET)"
	@echo ""
	@echo "Database: postgresql://postgres:editalshield2024@localhost:5432/editalshield"
	@echo "pgAdmin: http://localhost:5050 (admin@editalshield.com / admin123)"
	@echo ""
	@echo "Next steps:"
	@echo "  1. make train       - Train the ML model"
	@echo "  2. make db-shell    - Explore the database"
	@echo ""
