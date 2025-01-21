check: check_ruff check_mypy check_bandit tests

check_ruff: | venv3.11
	venv3.11/bin/ruff check --select ALL --ignore D202,D203,D213,I001,DTZ011

check_mypy: | venv3.11
	venv3.11/bin/mypy --strict src/*.py

check_bandit: | venv3.11
	venv3.11/bin/bandit -r src

tests: | venv3.11
	cd tests && ../venv3.11/bin/pytest --cov-report term-missing --cov=src .

venv3.11:
	python3.11 -mvenv venv3.11
	. venv3.11/bin/activate && pip install -r requirements.txt

run: check
	cd src && ../venv3.11/bin/fastapi dev main.py

.PHONY: check check_ruff check_mypy check_bandit tests run
