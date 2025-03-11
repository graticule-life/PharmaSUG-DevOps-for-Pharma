# Variables

# Define renv paths
RENV_BASE_DIR := $(PWD)/renv
RENV_PATHS_CACHE := $(RENV_BASE_DIR)/library

# Default target
all: setup
	

# Install dependencies using uv and pyproject.toml
.PHONY: install
install:
	@echo "Installing dependencies..."
	@pip install -e .

# Initial setup process; Python and R dependencies are installed
.PHONY: setup
setup: install rsetup

.PHONY: rsetup
rsetup:
	@echo "Checking for renv.lock file..."
	@if [ ! -f "renv.lock" ]; then \
		echo "Warning: renv.lock file not found. Unable to install dependencies..."; \
	else \
	    echo "R version: $$(Rscript --version)"; \
        echo "Using R cache at $(RENV_PATHS_CACHE)"; \
        Rscript -e 'renv::activate(); renv::restore(prompt = FALSE); install.packages("IRkernel"); renv::status()'; \
	fi
