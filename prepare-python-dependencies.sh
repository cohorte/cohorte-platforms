#!/bin/bash

echo "[INFO] Preparing Python dependencies..."

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

# Install dependencies
pip install --upgrade --index-url=$INDEX_URL -r requirements.txt

# Copy dependencies to home/lib
## cleanup home/lib directory
mv home/lib/README $VENV_NAME
rm -rf home/lib/*
mv $VENV_NAME/README home/lib
## copy python packages
### Jsonrpclib
mv tmp_venv/lib/python3.4/site-packages/jsonrpclib home/lib
### sleekxmpp
mv tmp_venv/lib/python3.4/site-packages/sleekxmpp home/lib
### requests
mv tmp_venv/lib/python3.4/site-packagesrequestshome/lib
### Herald
mv tmp_venv/lib/python3.4/site-packages/herald home/lib
### JPYPE
mv tmp_venv/lib/python3.4/site-packages/_jpype.so home/lib
mv tmp_venv/lib/python3.4/site-packages/jpype home/lib
mv tmp_venv/lib/python3.4/site-packages/jpypex home/lib
### iPOPO
mv tmp_venv/lib/python3.4/site-packages/pelix home/lib

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

