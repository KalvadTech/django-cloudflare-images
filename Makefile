all: install

install:
	python -m venv env
	. env/bin/activate && pip install -e .[dev]

clean:
	rm -rf env/
	rm -rf django_cloudflare_images.egg-info/
	rm -rf build/
	rm -rf dist/

format:
	. env/bin/activate && black . --exclude=env

test:
	. env/bin/activate && DJANGO_SETTINGS_MODULE=tests.settings django-admin test

package-develop:
	. env/bin/activate && python setup.py develop

package-build:
	. env/bin/activate && python setup.py build

package-install:
	. env/bin/activate && python setup.py install

package-sdist:
	. env/bin/activate && python setup.py sdist
