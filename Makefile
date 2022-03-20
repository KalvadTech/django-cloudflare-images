all: install

install:
	python -m venv env
	. env/bin/activate && pip install -e .[dev]

clean:
	rm -rf env/
	rm -rf django_cloudflare_images.egg-info/

format:
	. env/bin/activate && black . --exclude=env

test:
	DJANGO_SETTINGS_MODULE=tests.settings django-admin test

package:
	. env/bin/activate && python setup.py develop
