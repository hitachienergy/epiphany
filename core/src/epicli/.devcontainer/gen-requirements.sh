# Script that will generate requirements.txt from Pipfile.
pipenv lock -r --pre > requirements.txt  
sed -i '1,2d' requirements.txt  