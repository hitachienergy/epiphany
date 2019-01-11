# To work arround the fact that some of our scripts rely on GIT
# to get the Epiphany engine root directory we need to initialize
# it as a git repo. The GIT_DISCOVERY_ACROSS_FILESYSTEM must be set
# to 1 to deal with the build directory beeing a mounted volume.
echo 'Setup GIT'
cd  /epiphany
git init --quiet
export GIT_DISCOVERY_ACROSS_FILESYSTEM=1

echo 'Start BASH'
/bin/bash
