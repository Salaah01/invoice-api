test-cov:
	coverage run --source='.' manage.py test
	coverage html
	coverage report

define update_readme_cov =
	bash update_readme_cov.sh
endef

update-readme-cov:
	$(update_readme_cov)

update-python-pkgs:
	pip-compile requirements.in
