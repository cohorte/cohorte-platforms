#!/bin/sh

echo "----- update composition file"
echo "      COMPOSITION_FILE = $COMPOSITION_FILE"
RUN_SERVICE_FILE=/opt/run_service
echo "---- check if $RUN_SERVICE_FILE exists "
if [ -f $RUN_SERVICE_FILE ]; then	
	echo "--- $RUN_SERVICE_FILE exists "
	echo "--- variable : COMPOSITION_FILE=$COMPOSITION_FILE "
	
	SED_PARAM=s#COMPOSITION_FILE=.*#COMPOSITION_FILE=$COMPOSITION_FILE#g
	if [ -n "$COMPOSITION_FILE" ] ; then 
		echo "--- replace composition file to launch : cmd = [sed -i $SED_PARAM $RUN_SERVICE_FILE] "
		sed -i "$SED_PARAM" $RUN_SERVICE_FILE
	fi
fi