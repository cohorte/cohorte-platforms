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
DIRECTORY="/root/docker/node-devices"
DOCKER_REPOSITORY="cohorte/node-devices"

DOCKER_TAG=$1
DOCKER_USER=$2
DOCKER_PASSWORD=$3
DOCKER_ARM_HOST=$4
ID_RSA=$5
echo "DOCKER_USER=$DOCKER_USER"
echo "DOCKER_PASSWORD=$DOCKER_PASSWORD"
echo "DOCKER_ARM_HOST=$DOCKER_ARM_HOST"
echo "ID_RSA=$ID_RSA"


DOCKER_REGISTRY="dr.cohorte.tech"

# download get-pip 

cp -r $DIR/node/install $DIRECTORY/install
cd $DIRECTORY
wget https://bootstrap.pypa.io/get-pip.py


bash $DIR/build_image.sh "$DIRECTORY" "$DOCKER_REPOSITORY" "$DOCKER_TAG" "$DOCKER_USER" "$DOCKER_PASSWORD" "$DOCKER_REGISTRY"
