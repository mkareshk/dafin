SHELL := /bin/bash

install:
	pip install .

install_code:
	pip install -e .[test]

test:
	pytest --cov-report term-missing --cov=dafin tests/

uml:
	pyreverse -o png -p dafin dafin

install_precommit:
	pip install pre-commit
	pre-commit install

run_precommit:
	pre-commit run --all-files

install_dev:
	python -m pip install -U pip
	pip install -e .
	pip install -e ."[dev]"
	pre-commit install
	pre-commit autoupdate
	pre-commit run --all-files
