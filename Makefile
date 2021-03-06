SHELL=/bin/bash
.DEFAULT_GOAL=unit

clean:
	@find . -iname '*.py[co]' -delete
	@find . -name '__pycache__' -prune | xargs rm -rf # clean __pycache__ dirs build by py.test

coverage:
	PYTHONPATH=. py.test tests/unit --cov-report=html --cov=builder ${ARGS}

unit:
	PYTHONPATH=. py.test ${ARGS} tests/unit

local_config:
	cp builder/config/local.py.example builder/config/local.py

upgrade_db:
	python manage.py db upgrade

migrate_db:
	python manage.py db migrate

runserver:
	python manage.py runserver

deps:
	pip install -r requirements/dev.txt

init_env:
	pip install -r requirements/dev.txt
	cp builder/config/local.py.example builder/config/local.py
	python manage.py db upgrade
	python scripts/add_some_users.py
