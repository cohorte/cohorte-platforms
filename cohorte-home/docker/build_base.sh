#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIRECTORY="$DIR/base"
DOCKER_REPOSITORY="cohorte/base"

DOCKER_TAG="1.5-alpine"
DOCKER_USER=$1
DOCKER_PASSWORD=$2

DOCKER_REGISTRY="dr.cohorte.tech"

echo -e "\x1B[1;32m[INFO] Building Image [$DOCKER_REPOSITORY:$DOCKER_TAG] located on [$DIRECTORY]\x1B[0m"

bash $DIR/build_image.sh "$DIRECTORY" "$DOCKER_REPOSITORY" "$DOCKER_TAG" Dockerfile "$DOCKER_USER" "$DOCKER_PASSWORD" "$DOCKER_REGISTRY"

docker history "$DOCKER_REPOSITORY:$DOCKER_TAG"
