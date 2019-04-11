cd  /epiphany/
git init -q
export GIT_DISCOVERY_ACROSS_FILESYSTEM=1
echo "Preparing credentials"
bash core/core/src/docker/test-CI/prepare_sp.sh
cd  /epiphany/core
echo
echo "Epiphany build for resource group $RESOURCE_GROUP started..."
bash epiphany -a -b -i -f infrastructure/$RESOURCE_GROUP -t /infrastructure/epiphany-qa-template

status=$?

if [ $status -eq 0 ]
then
	echo
	echo "Epiphany build for resource group $RESOURCE_GROUP completed"
	echo
	cd /epiphany/core/core/test/serverspec
	echo "Serverspec tests for resource group $RESOURCE_GROUP started..."
	rake inventory=/epiphany/core/build/epiphany/$RESOURCE_GROUP/inventory/development user=operations keypath=/tmp/keys/id_rsa spec:all
	echo "Serverspec tests for resource group $RESOURCE_GROUP finished"
	echo
else
  echo "Epiphany build failed!";
  exit 1;
fi
