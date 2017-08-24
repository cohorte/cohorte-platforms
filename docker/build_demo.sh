#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIRECTORY="$DIR/demo"
DOCKER_REPOSITORY="cohorte/demo"

DOCKER_TAG=$1
DOCKER_USER=$2
DOCKER_PASSWORD=$3

DOCKER_REGISTRY="dr.cohorte.tech"


echo -e "\x1B[1;32m[INFO] Building Image [$DOCKER_REPOSITORY:$DOCKER_TAG] located on [$DIRECTORY]\x1B[0m"

bash $DIR/build_image.sh "$DIRECTORY" "$DOCKER_REPOSITORY" "$DOCKER_TAG" "$DOCKER_USER" "$DOCKER_PASSWORD" "$DOCKER_REGISTRY"
