#!/bin/bash

echo "[INFO] Preparing Python dependencies..."

# Clean up
mkdir tmp
mv home/lib/README tmp
rm -rf home/lib/*
mv tmp/README home/lib
rm -rf tmp

# analyse parameters
if test "$1" == "minimal"; then
exit;
fi

# Set up the virtual environment
VENV_NAME=tmp_venv
INDEX_URL=http://forge.isandlatech.com:3080/devpi/jenkins/cohorte/+simple/
rm -fr $VENV_NAME
virtualenv $VENV_NAME -p python3 || return 1
PATH=$WORKSPACE/$VENV_NAME/bin:$PATH
. $VENV_NAME/bin/activate

# Install test and deployment tools
pip install --upgrade --index-url=$INDEX_URL pip setuptools || return 2
pip install --upgrade --index-url=$INDEX_URL wheel || return 2
pip install --upgrade --index-url=$INDEX_URL nose || return 2
pip install --upgrade --index-url=$INDEX_URL devpi-client || return 2

# install JPype
# JPype1-py3==0.5.5.2
if test "$1" == "macosx"; then
python deps.py --package=JPype1-py3 --platform=darwin --install
elif test "$1" == "linux"; then
python deps.py --package=JPype1-py3 --platform=linux-x86_64 --install
elif test "$1" == "win32"; then
echo "[ERROR] windows is not yet supported for JPype binaries!"
fi

# Install dependencies
pip install --upgrade --index-url=$INDEX_URL -r requirements.txt

# Copy dependencies to home/lib
## cleanup home/lib directory

## copy python packages
PYTHON_INSTALLED=`ls $VENV_NAME/lib`
### Jsonrpclib
mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/jsonrpclib home/lib
### sleekxmpp
mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/sleekxmpp home/lib
### requests
mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/requests home/lib
### Herald
mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/herald home/lib
### JPYPE
mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/_jpype.so home/lib
mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/jpype home/lib
mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/jpypex home/lib
### iPOPO
mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/pelix home/lib
### Cohorte Python
mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/cohorte home/lib

# Install project
#pip install --index-url=$INDEX_URL .

# Run tests
# nosetests tests || return 3

# Deploy
#devpi use $DEVPI_URL --index-url=$INDEX_URL
#devpi login $devpi_user --password=$devpi_password --index-url=$INDEX_URL
#devpi use $devpi_index --index-url=$INDEX_URL
#devpi upload --no-vcs --formats=$devpi_formats --index-url=$INDEX_URL

# Clean up
deactivate
rm -fr $VENV_NAME

echo "[INFO] Python dependencies are installed on home/lib"

