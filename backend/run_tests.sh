#!/bin/bash

# Run all tests for the GradientLab backend

# Set environment variables for testing
export FLASK_ENV=testing
export DATABASE_URL=sqlite:///:memory:
export JWT_SECRET_KEY=test_secret_key

# Run pytest with coverage
python -m pytest tests/ -v --cov=. --cov-report=term-missing

# Return the exit code of pytest
exit $?
