#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $DIR

DIRECTORY="/root/docker/runtime-arm64v8"
DOCKER_REPOSITORY="cohorte/runtime-arm64v8"

DOCKER_TAG=$1
DOCKER_USER=$2
DOCKER_PASSWORD=$3
DOCKER_ARM_HOST=$3
ID_RSA=$4
echo "DOCKER_USER=$DOCKER_USER"
echo "DOCKER_PASSWORD=$DOCKER_PASSWORD"
echo "DOCKER_ARM_HOST=$DOCKER_ARM_HOST"
echo "ID_RSA=$ID_RSA"

DOCKER_REGISTRY="dr.cohorte.tech"

echo -e "\x1B[1;32m[INFO] Building Image [$DOCKER_REPOSITORY:$DOCKER_TAG] located on [$DIRECTORY]\x1B[0m"

mkdir -p $DIR/runtime-arm64v8/install
rm -rf $DIR/runtime-arm64v8/install/*



cp $DIR/../target/cohorte-*-distribution.tar.gz $DIR/runtime-arm64v8/install/cohorte.tar.gz


echo -e "\x1B[1;32m[INFO] Building Image [$DOCKER_REPOSITORY:$DOCKER_TAG] located on [$DIRECTORY]\x1B[0m"
echo "scp -r -o StrictHostKeyChecking=no -i $ID_RSA $DIR/runtime-arm64v8/ root@$DOCKER_ARM_HOST:/root/docker/"
#scp -r -o StrictHostKeyChecking=no -i $ID_RSA $DIR/runtime-arm64v8/ root@$DOCKER_ARM_HOST:/root/docker/
ssh -o StrictHostKeyChecking=no -i $ID_RSA  root@$DOCKER_ARM_HOST 'cat | bash /dev/stdin' "$DIRECTORY $DOCKER_REPOSITORY $DOCKER_TAG $DOCKER_USER $DOCKER_PASSWORD $DOCKER_REGISTRY" < $DIR/build_image.sh 
