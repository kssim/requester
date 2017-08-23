init:
	pip install -r requirements.txt

coverage:
	py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=requester tests
