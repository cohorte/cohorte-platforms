#!/bin/bash

echo "[INFO] Preparing Python dependencies..."

# analyse parameters
if test "$1" == "minimal"; then
exit;
fi

# generate conf/version.js file
timestamp=$(date +"%Y%m%d-%H%M%S")
dist=$1
version_full=$2
version_num=$(echo $2 | cut -d\- -f 1)
version_stage=$(echo $2 | cut -d\- -f 2)
git_branch=$(git branch | grep \* | cut -d ' ' -f2)
git_commit=$(git rev-parse HEAD)
stage=release
if test "$version_stage" == "SNAPSHOT"; then
	stage="dev"
fi
echo "{"      													> conf/version.js 
echo "	\"distribution\" : \"cohorte-${dist}-distribution\","	>> conf/version.js
echo "	\"stage\" : \"${stage}\","								>> conf/version.js
echo "	\"version\" : \"${version_num}\","						>> conf/version.js
echo "	\"timestamp\" : \"${timestamp}\","						>> conf/version.js
echo "	\"git_branch\" : \"${git_branch}\","						>> conf/version.js
echo "	\"git_commit\" : \"${git_commit}\""						>> conf/version.js
echo "}"														>> conf/version.js

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


# Set up the virtual environment
VENV_NAME=tmp_venv
INDEX_URL=http://devpi.cohorte.tech/root/cohorte/+simple/
rm -fr $VENV_NAME
virtualenv $VENV_NAME -p python || return 1
PATH=$WORKSPACE/$VENV_NAME/bin:$PATH
. $VENV_NAME/bin/activate

# Install test and deployment tools
PIP_HOST=devpi.cohorte.tech
#--trusted-host $PIP_HOST
pip --version
pip install --force --upgrade --index-url=$INDEX_URL pip==8.1.2 setuptools  #|| return 2
pip --version 
pip install --upgrade --index-url=$INDEX_URL --trusted-host=$PIP_HOST wheel #|| return 2
pip install --upgrade --index-url=$INDEX_URL --trusted-host=$PIP_HOST nose #|| return 2
pip install --upgrade --index-url=$INDEX_URL --trusted-host=$PIP_HOST devpi-client #|| return 2

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
pip install --upgrade -r requirements_ipopo.txt
pip install --upgrade --index-url=$INDEX_URL --trusted-host=$PIP_HOST -r requirements.txt

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
#mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/herald repo
cp -r /var/jenkins_home/workspace/cohorte/cohorte-herald/python/herald repo/

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
#mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/cohorte repo
cp -r /var/jenkins_home/workspace/cohorte/cohorte-runtime/python/cohorte repo/
### Cohorte Webadmin
#mv tmp_venv/lib/$PYTHON_INSTALLED/site-packages/webadmin repo

# Clean up
deactivate
rm -fr $VENV_NAME

echo "[INFO] Python dependencies are installed on repo"

