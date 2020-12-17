#!/bin/bash

##
# HISTORY
#
# 1.2.1:
#   - update to cohorte platform 1.2.1
# 1.12.0_2: 
#   - MOD_BD_20161222: modify run_service script to set COMPOSITION_FILE as variable.
# 1.12.0_1: 
#   - introduces "boot.sh" script to start systemd after another user provide initialization scripts "init.sh".
#
##

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIRECTORY="$DIR/node-java-ubuntu"
DOCKER_REPOSITORY="cohorte/node"

DOCKER_TAG=$1-java-ubuntu
DOCKER_USER=$2
DOCKER_PASSWORD=$3

DOCKER_REGISTRY="dr.cohorte.tech"

# download get-pip 
cd $DIR/node/install/
wget https://bootstrap.pypa.io/get-pip.py


echo -e "\x1B[1;32m[INFO] Building Image [$DOCKER_REPOSITORY:$DOCKER_TAG] located on [$DIRECTORY]\x1B[0m"

bash $DIR/build_image.sh "$DIRECTORY" "$DOCKER_REPOSITORY" "$DOCKER_TAG" Dockerfile "$DOCKER_USER" "$DOCKER_PASSWORD" "$DOCKER_REGISTRY"
