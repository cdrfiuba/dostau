all: install

install:
	python setup.py install --user

test: install
	python UnitTests.py

coverage: install
	python-coverage run --source="py3pi" UnitTests.py
	python-coverage report -m

clean:
	python-coverage erease
	python setup.py clean
		
