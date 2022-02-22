SHELL := /bin/bash

test:
	@rm -rf venv_test
	@python3 -m venv venv_test \
		&& source ./venv_test/bin/activate \
		&& python3 -m pip install -U pip setuptools wheel pytest \
		&& pip3 wheel --only-binary=:all: --no-deps . \
		&& pip3 install dafin-*.whl \
		&& pytest
	@rm dafin-*.whl
	@rm -rf venv_test

test_cov:
	pytest --cov-report term-missing --cov=dafin tests/

test_cov_docker:
	docker build -t dafin:test -f Dockerfile.test .
	dokcer run  dafin:test