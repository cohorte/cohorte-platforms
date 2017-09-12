#!/bin/bash

USERNAME=$1
PASSWORD=$2
FELIX_VERSION=5.4.0

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR/target

for file in ./*
do
	curl -v --user "$USERNAME:$PASSWORD" --upload-file ${file} https://nrm.cohorte.tech/repository/felix-p2/${FELIX_VERSION}/${file}
done;

for file in plugins/*
do
	curl -v --user "$USERNAME:$PASSWORD" --upload-file ${file} https://nrm.cohorte.tech/repository/felix-p2/${FELIX_VERSION}/${file}
done;