# Script to prepare for BDS scan. It wil build the Epicli distribtion wheel 
# and from that download and build/extract all used python dependencies 
# to the externals directory for inclusion with the BDS scan.
sh ./build-wheel.sh
pip download --no-clean --no-binary all -d $PWD/external/packages/ --build $PWD/external/build/ $PWD/dist/epicli-0.3.0-py3-none-any.whl
