SHELL := /bin/bash

install:
	pip3 install .

install_code:
	pip3 install -e .

test:
	pytest --cov-report term-missing --cov=dafin tests/

uml:
	pyreverse -o png -p dafin dafin 
