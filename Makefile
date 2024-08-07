default: create-requirements lint

.PHONY: create-requirements
create-requirements:
	poetry export --format=requirements.txt > requirements.txt

.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY: run
run:
	gunicorn incident_reporting.main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --reload

.PHONY: deploy
deploy:
	gcloud app deploy app.yaml
