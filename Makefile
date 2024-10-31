install_dev:
	pip install -r requirements/dev.txt

run_tests:
	pytest run_tests

check_code_style:
	## pylint
	pylint --disable=C0114,C0115,C0116 app

	## black
	black --check app

	##mypy
	mypy app

