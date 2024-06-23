.PHONY: lint mypy test

lint:
	poetry run sh -c 'set -x && \
	ruff format tp/ test/ \
	&& ruff check --fix --show-fixes tp/ test/ \
	&& bandit -c pyproject.toml -r tp/'

mypy:
	poetry run mypy tp/ test/

test:
	poetry run pytest --cov --cov-report term-missing:skip-covered

export_deps:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
