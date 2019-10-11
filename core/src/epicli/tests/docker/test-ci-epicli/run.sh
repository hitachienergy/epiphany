#!/bin/bash
echo "Starting Epiphany build for cluster $CLUSTER_NAME"

epicli apply -f "/shared/$CLUSTER_NAME/$CLUSTER_NAME.yml"

if [[ $? -eq 0 ]]
then
	echo
	echo "Epiphany build for cluster $CLUSTER_NAME completed successfully"
	echo
	echo "Serverspec tests for cluster $CLUSTER_NAME started..."
	rake inventory="/shared/build/$CLUSTER_NAME/inventory" user=$ADMIN_USERNAME keypath=$KEY_PATH spec:all
	echo "Serverspec tests for cluster $CLUSTER_NAME finished"
	echo
else
    echo
    echo "Epiphany build for cluster $CLUSTER_NAME FAILED!"
	echo
    exit 1
fi
