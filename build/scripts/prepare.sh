#!/bin/bash

echo "[INFO] Preparing Python dependencies..."

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
pip install --force --upgrade --index-url=$INDEX_URL pip==1.5.6 setuptools #|| return 2
pip install --upgrade --index-url=$INDEX_URL wheel #|| return 2
pip install --upgrade --index-url=$INDEX_URL nose #|| return 2
pip install --upgrade --index-url=$INDEX_URL devpi-client #|| return 2

# install JPype
# JPype1-py3==0.5.5.2
if test "$1" == "macosx"; then
# python build/scripts/deps.py --package=JPype1-py3 --platform=darwin --install
echo "[WARNING] copying jpype files directly to repo folder"
cp -r build/extra/macosx/* repo	
elif test "$1" == "linux"; then
#python build/scripts/deps.py --package=JPype1-py3 --platform=linux-x86_64 --install
echo "[WARNING] copying jpype files directly to repo folder"
cp -r build/extra/linux/* repo	
elif test "$1" == "windows"; then
echo "[WARNING] copying jpype files directly to repo folder"
cp -r build/extra/windows/* repo	
fi

# Install dependencies
pip install --upgrade --index-url=$INDEX_URL -r build/scripts/requirements.txt

# Copy dependencies to repo

## copy python packages
PYTHON_INSTALLED=`ls $VENV_NAME/lib`
### Jsonrpclib
mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/jsonrpclib repo
### sleekxmpp
mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/sleekxmpp repo
### requests
mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/requests repo
### Herald
mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/herald repo

### JPYPE
#if test "$1" != "windows"; then
#	if test "$1" != "python"; then
#		mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/_jpype*.so repo
#		mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/jpype repo
#		mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/jpypex repo
#	fi
#fi
### iPOPO
mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/pelix repo
### Cohorte Python
mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/cohorte repo
### Cohorte Webadmin
#mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/webadmin repo

# Clean up
deactivate
rm -fr $VENV_NAME

echo "[INFO] Python dependencies are installed on repo"

