# UIOTA Ontogenetic Intelligence Framework
# Complete sovereign computing development environment

.PHONY: help install install-deps install-python install-node install-rust install-go \
        test test-python test-rust test-node test-go \
        build build-dashboard build-simulation \
        run run-simulation run-dashboard \
        clean format lint air-gap-verify mini-os

# Default target
help: ## Show this help message
	@echo "UIOTA Ontogenetic Intelligence Framework"
	@echo "======================================="
	@echo ""
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Installation targets
install: install-deps install-python install-node install-rust install-go ## Install complete development environment

install-deps: ## Install system dependencies
	@echo "Installing system dependencies..."
	sudo apt update
	sudo apt install -y \
		build-essential \
		cmake \
		pkg-config \
		libssl-dev \
		curl \
		wget \
		git \
		vim \
		neovim \
		python3 \
		python3-pip \
		python3-venv \
		nodejs \
		npm

install-python: ## Install Python environment
	@echo "Installing Python environment..."
	python3 -m venv venv
	source venv/bin/activate && pip install --upgrade pip setuptools wheel
	source venv/bin/activate && pip install -r requirements.txt

install-node: ## Install Node.js dependencies
	@echo "Installing Node.js dependencies..."
	cd web-interface && npm install

install-rust: ## Install Rust toolchain
	@echo "Installing Rust toolchain..."
	curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
	source ~/.cargo/env
	rustup component add clippy rustfmt

install-go: ## Install Go dependencies
	@echo "Installing Go dependencies..."
	go mod download

# Testing targets
test: test-python test-rust test-node test-go ## Run all tests

test-python: ## Run Python tests
	@echo "Running Python tests..."
	source venv/bin/activate && python -m pytest tests/ -v

test-rust: ## Run Rust tests
	@echo "Running Rust tests..."
	cargo test

test-node: ## Run Node.js tests
	@echo "Running Node.js tests..."
	cd web-interface && npm test

test-go: ## Run Go tests
	@echo "Running Go tests..."
	go test ./...

# Build targets
build: build-dashboard build-simulation ## Build all components

build-dashboard: ## Build React dashboard
	@echo "Building OGI dashboard..."
	cd web-interface && npm run build

build-simulation: ## Build simulation components
	@echo "Building simulation components..."
	source venv/bin/activate && python src/ogi_simulation.py --build-only

# Run targets
run: run-simulation ## Run OGI simulation

run-simulation: ## Run the OGI vs FL simulation
	@echo "Running OGI simulation..."
	source venv/bin/activate && python src/ogi_simulation.py

run-dashboard: ## Run the interactive dashboard
	@echo "Starting OGI dashboard..."
	cd web-interface && npm start

run-api: ## Run the FastAPI backend
	@echo "Starting OGI API..."
	source venv/bin/activate && uvicorn src.api:app --reload

# Development targets
format: ## Format all source code
	@echo "Formatting code..."
	source venv/bin/activate && black src/ tests/
	cd web-interface && npm run format
	cargo fmt

lint: ## Lint all source code
	@echo "Linting code..."
	source venv/bin/activate && flake8 src/ tests/
	cd web-interface && npm run lint
	cargo clippy -- -D warnings

air-gap-verify: ## Verify air-gap compliance
	@echo "Verifying air-gap compliance..."
	./scripts/air-gap-verify.sh

# Mini OS development
mini-os: ## Build UIOTA Mini OS (requires Alpine environment)
	@echo "Building UIOTA Mini OS with OGI integration..."
	./scripts/build-mini-os.sh

mini-os-test: ## Test Mini OS in virtual environment
	@echo "Testing UIOTA Mini OS..."
	./scripts/test-mini-os.sh

# Deployment targets
deploy-dashboard: ## Deploy dashboard to GitHub Pages
	@echo "Deploying dashboard..."
	./deploy_dashboard.sh

# Research targets
research-paper: ## Generate research paper
	@echo "Generating research paper..."
	source venv/bin/activate && python scripts/generate_paper.py

benchmark: ## Run performance benchmarks
	@echo "Running benchmarks..."
	source venv/bin/activate && python scripts/benchmark.py

# Maintenance targets
clean: ## Clean build artifacts
	@echo "Cleaning build artifacts..."
	rm -rf venv/
	rm -rf web-interface/node_modules/
	rm -rf web-interface/build/
	cargo clean
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete

update-deps: ## Update all dependencies
	@echo "Updating dependencies..."
	source venv/bin/activate && pip install --upgrade -r requirements.txt
	cd web-interface && npm update
	cargo update

# Documentation
docs: ## Generate documentation
	@echo "Generating documentation..."
	source venv/bin/activate && sphinx-build -b html docs/ docs/_build/

# Complete development setup
dev-setup: install air-gap-verify test ## Complete development environment setup
	@echo ""
	@echo "🧬 UIOTA Ontogenetic Intelligence Framework"
	@echo "==========================================="
	@echo ""
	@echo "✅ Development environment setup complete!"
	@echo ""
	@echo "Quick start:"
	@echo "  make run-simulation    # Run OGI vs FL simulation"
	@echo "  make run-dashboard     # Start interactive dashboard"
	@echo "  make mini-os          # Build UIOTA Mini OS"
	@echo ""
	@echo "🌐 Dashboard: http://localhost:3000"
	@echo "📊 API: http://localhost:8000"
	@echo "📋 Mini OS Roadmap: docs/MINI_OS_ROADMAP.md"

.DEFAULT_GOAL := help