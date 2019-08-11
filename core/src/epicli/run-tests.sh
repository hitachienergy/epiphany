# Run the python test for Epicli
mkdir -p tests_result
python -m pytest ./tests/ | tee tests_result/result.txt
echo "Done running tests. See tests_result/result.txt"