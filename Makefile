all: clean install test

install:
	python -m venv env
	. env/bin/activate && pip install -e .[dev] && pip install --upgrade pip

clean:
	rm -rf env/
	rm -rf .tox/
	rm -rf django_cloudflare_images.egg-info/
	rm -rf build/
	rm -rf dist/

format:
	. env/bin/activate && black . --extend-exclude=env

test:
	. env/bin/activate && tox

package:
	. env/bin/activate && python -m build
