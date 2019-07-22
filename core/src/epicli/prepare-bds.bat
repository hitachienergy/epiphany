:: Script to prepare for BDS scan. It wil build the Epicli distribtion wheel
:: and from that download and build/extract all used python dependencies
:: to the externals directory for inclusion with the BDS scan.
call build-wheel.bat
pip download --no-clean --no-binary all -d %cd%/external/packages/ --build %cd%/external/ %cd%/dist/epicli-0.3.0-py3-none-any.whl
rmdir /Q /S %cd%\external\packages\
rmdir /Q /S %cd%\external\epicli\
