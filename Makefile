.PHONY: lint
lint:
	poetry export --without-hashes --format=requirements.txt > requirements.txt
	pre-commit run --all-files

.PHONY: run
run:
	python -m incident_reporting
