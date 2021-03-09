#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIRECTORY="$DIR/base"
DOCKER_REPOSITORY="cohorte/base"

DOCKER_USER=$1
DOCKER_PASSWORD=$2

DOCKER_REGISTRY="dr.cohorte.tech"

echo -e "\x1B[1;32m[INFO] Building Image [$DOCKER_REPOSITORY:1809] located on [$DIRECTORY]\x1B[0m"

bash $DIR/build_image.sh "$DIRECTORY" "$DOCKER_REPOSITORY" "1.5-win1909" Dockerfile-1909 "$DOCKER_USER" "$DOCKER_PASSWORD" "$DOCKER_REGISTRY"

docker history "$DOCKER_REPOSITORY:$DOCKER_TAG"
