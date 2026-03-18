.PHONY: install test test-cov lint fmt run shell db-init clean

install:
	hatch env create
	hatch run pip install -e .

test:
	hatch run test

test-cov:
	hatch run test-cov

lint:
	hatch run lint

fmt:
	hatch run fmt

run:
	hatch run cashflow --help

shell:
	hatch shell

db-init:
	hatch run python -c "from cashflow.infrastructure.database import init_db; init_db()"

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.pytest_cache' -delete
	rm -rf cashflow.db