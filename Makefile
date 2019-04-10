language = python
project_name = analyser
environment = env
manage = manage.py
activate = . $(environment)/bin/activate

venv:
	$(language) -m venv $(environment)
	$(activate)

migrate:
	$(activate)
	$(environment)/bin/pip install -r requirements.txt
	$(environment)/bin/$(language) $(manage) makemigrations manager
	$(environment)/bin/$(language) $(manage) migrate

run:
	$(activate)
	$(environment)/bin/$(language) $(manage) createsuperuser
	$(environment)/bin/$(language) $(manage) runserver


install: venv migrate default-data
all: install install-saracore run 
