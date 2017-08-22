#!/bin/bash

USERNAME=$1
PASSWORD=$2
COHORTE_VERSION=$3

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR/target/repository

for file in ./*
do
	curl -v --user "$USERNAME:$PASSWORD" --upload-file ${file} https://nrm.cohorte.tech/repository/cohorte-p2/${COHORTE_VERSION}/${file}
done;

for file in plugins/*
do
	curl -v --user "$USERNAME:$PASSWORD" --upload-file ${file} https://nrm.cohorte.tech/repository/cohorte-p2/${COHORTE_VERSION}/${file}
done;