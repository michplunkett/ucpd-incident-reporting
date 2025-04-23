.DEFAULT_GOAL := lint

.PHONY: env
env:
	uv venv

.PHONY: lint
lint: create-requirements
	pre-commit run --all-files

.PHONY: create-requirements
create-requirements:
	uv pip compile --generate-hashes pyproject.toml > requirements.txt

.PHONY: run
run:
	gunicorn incident_reporting.main:app --worker-class uvicorn.workers.UvicornWorker --reload

.PHONY: deploy
deploy:
	gcloud app deploy app.yaml
