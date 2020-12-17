#!/bin/bash
COMPOSITION_FILE=composition.js
export JAVA_HOME=/opt/java
export COHORTE_HOME=/opt/cohorte
export COHORTE_BASE=/opt/node
bash ${COHORTE_HOME}/bin/cohorte-start-node --base ${COHORTE_BASE} --use-config ${COHORTE_BASE}/conf/run.js --composition-file ${COMPOSITION_FILE} -d -v -c --console false --interpreter python3 --http-port 9000 --shell-port 9001 $* &
