test:
	pipenv run pytest

format:
	pipenv run black ./**/*.py

lint:
	pipenv run flake8  && pipenv run black --check ./**/*.py
