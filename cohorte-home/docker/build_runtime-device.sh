#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $DIR

DIRECTORY="/root/docker/runtime-devices"
DOCKER_REPOSITORY="cohorte/runtime-devices"

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

echo -e "\x1B[1;32m[INFO] Building Image [$DOCKER_REPOSITORY:$DOCKER_TAG] located on [$DIRECTORY]\x1B[0m"

mkdir -p $DIR/runtime-devices/install
rm -rf $DIR/runtime-devices/install/*



cp $DIR/../target/cohorte-*-distribution.tar.gz $DIR/runtime-devices/install/cohorte.tar.gz


bash $DIR/build_image.sh "$DIRECTORY" "$DOCKER_REPOSITORY" "$DOCKER_TAG" "$DOCKER_USER" "$DOCKER_PASSWORD" "$DOCKER_REGISTRY"