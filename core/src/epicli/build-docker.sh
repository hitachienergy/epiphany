# Script to build the Epicli docker image. It wil build the Epicli distribtion wheel 
# and from use that to provision the docker image.
sh ./build-wheel.sh
read EPICLI_VERSION < cli/version.txt.py
docker build -t epicli -f Dockerfile . --build-arg EPICLI_VERSION=$EPICLI_VERSION