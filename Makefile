default: create-requirements lint

.PHONY: create-requirements
create-requirements:
	poetry export --without-hashes --format=requirements.txt > requirements.txt

.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY: run
run:
	python app.py
