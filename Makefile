default: create-requirements lint

.PHONY: create-requirements
create-requirements:
	poetry export --without-hashes --format=requirements.txt > requirements.txt

.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY: run
run:
	uvicorn prijateli_tree.app.main:app --reload --host 0.0.0.0 --port 8000
