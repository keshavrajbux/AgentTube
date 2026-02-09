.PHONY: setup dev db-up db-down seed test clean

# Setup virtual environment and install dependencies
setup:
	cd backend && python -m venv venv && . venv/bin/activate && pip install -r requirements.txt

# Start development server
dev:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start database with Docker
db-up:
	docker-compose up -d db redis

# Stop database
db-down:
	docker-compose down

# Run full stack with Docker
docker-up:
	docker-compose up -d

# Seed sample data
seed:
	cd backend && python seed_data.py

# Run tests
test:
	cd backend && pytest

# Clean up
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
