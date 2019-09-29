
./skopeo_linux --version

PACKAGE_LIST=$(cat ./requirements.txt)
for package in $PACKAGE_LIST ; do
        echo $package
        apt-get install -y --download-only $package
done