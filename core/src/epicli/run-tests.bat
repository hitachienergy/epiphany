:: Run the python test for Epicli
mkdir -p tests_result
pipenv run python -m pytest ./tests/  > tests_result/result.txt
echo "Done running tests. See tests_result/result.txt"