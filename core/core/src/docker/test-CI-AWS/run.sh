function destroyEnvironment {
	cd /shared/$CLUSTER_NAME/terraform
	terraform init
	terraform destroy -auto-approve
}

epicli apply -f /shared/$CLUSTER_NAME/$CLUSTER_NAME.yml

status=$?

if [ $status -eq 0 ]
then
	echo
	echo "Epiphany build for cluster $CLUSTER_NAME completed"
	echo
	echo "Serverspec tests for cluster $CLUSTER_NAME started..."
	rake inventory=/shared/$CLUSTER_NAME/inventory user=$ADMIN_USERNAME keypath=$KEY_PATH spec:all
	echo "Serverspec tests for cluster $CLUSTER_NAME finished"
	destroyEnvironment 
	echo
else
    echo
    echo "Epiphany build for cluster $CLUSTER_NAME FAILED!"
	destroyEnvironment 
    exit 1
fi
