install_dev:
	pip install -r requirements/dev.txt

run_tests:
	pytest run_tests

check_code_style:
	## pylint
	pylint --disable=C0114,C0115,C0116 social_media

	## black
	black --check social_media

	##mypy
	mypy social_media

