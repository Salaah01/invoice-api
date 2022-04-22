tests-cov:
	coverage run --source='.' manage.py test
	coverage html
	coverage report