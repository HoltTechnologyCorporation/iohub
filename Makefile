.PHONY: build venv deps clean init ioweb tgram static run shell

build: venv deps init

venv:
	virtualenv -p python3 .env

deps:
	.env/bin/pip install -r requirements.txt

clean:
	find -name '*.pyc' -delete
	find -name '*.swp' -delete
	find -name '__pycache__' -delete

init:
	if [ ! -e var/run ]; then mkdir -p var/run; fi
	if [ ! -e var/log ]; then mkdir -p var/log; fi
	if [ ! -e static/components ]; then mkdir -p static/components; fi
	if [ ! -e static/assets ]; then mkdir -p static/assets; fi
	if [ ! -e static/collected ]; then mkdir -p static/collected; fi

ioweb:
	mkdir -p src
	if [ ! -e src/ioweb ]; then ln -s /web/ioweb src; fi
	if [ ! -e ioweb ]; then ln -s src/ioweb/ioweb; fi
	.env/bin/pip install -e src/ioweb

static:
	./manage.py collectstatic --link --noinput

run:
	./manage.py runserver --settings=project.settings_debug 0.0.0.0:8001

shell:
	./manage.py shell_plus
