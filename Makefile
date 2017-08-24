init:
	pip install -r requirements.txt

test:
	detox

flake8:
	flake8 --ignore=E501 requester

coverage:
	py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=requester tests
