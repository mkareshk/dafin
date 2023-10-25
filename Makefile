SHELL := /bin/bash

install:
	pip install .

install_code:
	pip install -e .[test]

test:
	pytest --cov-report term-missing --cov=dafin tests/

uml:
	pyreverse -o png -p dafin dafin 
