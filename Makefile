PYTHON = python3

.PHONY: install test clean

install:
	bash ./scripts/resolve-deps.sh

test:
	${PYTHON} setup.py pytest

clean:
	rm -rf .eggs .pytest_cache cp_screen.egg-info cpimgtxt.egg-info

