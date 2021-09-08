PYTHON = python3

.PHONY: build test clean

default: build

build:
	bash ./scripts/resolve-deps.sh

test:
	${PYTHON} setup.py pytest

clean:
	rm -rf .eggs .pytest_cache cp_screen.egg-info cpimgtxt.egg-info

