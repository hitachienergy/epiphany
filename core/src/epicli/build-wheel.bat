:: Script that will wil build the Epicli distribtion wheel.
pipenv lock -r > requirements.txt
pipenv run python setup.py bdist_wheel

