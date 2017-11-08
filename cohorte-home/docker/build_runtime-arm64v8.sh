#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $DIR

DIRECTORY="$DIR/runtime-arm64v8"
DOCKER_REPOSITORY="cohorte/runtime-arm64v8"

DOCKER_TAG=$1
DOCKER_USER=$2
DOCKER_PASSWORD=$3

DOCKER_REGISTRY="dr.cohorte.tech"

echo -e "\x1B[1;32m[INFO] Building Image [$DOCKER_REPOSITORY:$DOCKER_TAG] located on [$DIRECTORY]\x1B[0m"

mkdir -p $DIR/runtime-arm64v8/install
rm -rf $DIR/runtime-arm64v8/install/*

cp $DIR/../target/cohorte-*-distribution.tar.gz $DIR/runtime-arm64v8/install/cohorte.tar.gz

cp -r $DIR/../build/extra/arm64v8 $DIR/runtime-arm64v8/install/

bash $DIR/build_image.sh "$DIRECTORY" "$DOCKER_REPOSITORY" "$DOCKER_TAG" "$DOCKER_USER" "$DOCKER_PASSWORD" "$DOCKER_REGISTRY"