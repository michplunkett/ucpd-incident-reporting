BASEDIR=ucpd_incident_reporting

.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY: test
test:
	pytest -vs test/

.PHONY: test-and-fail
test-and-fail:
	pytest -vsx test/

.PHONY: run
run:
	python -m BASEDIR
