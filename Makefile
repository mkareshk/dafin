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
