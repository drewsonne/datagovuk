install: clean
	pip install -e .

build:
	python setup.py sdist bdist_wheel

release-test: clean build
	twine upload -r pypitest dist/*

release: clean build
	twine upload -r pypi dist/*

test: clean
	tox

test-server: clean
	devpi test route-registry

clean:
	rm -rf dist build *.egg-info MANIFEST .tox .eggs
