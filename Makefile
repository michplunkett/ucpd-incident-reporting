default: create-requirements lint

.PHONY: create-requirements
create-requirements:
	poetry export --format=requirements.txt > requirements.txt

.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY: run
run:
	gunicorn incident_reporting.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
