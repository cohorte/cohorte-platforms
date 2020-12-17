#!/bin/bash
echo "--- Boot of Cohorte Container..."
#./opt/init.sh
# check what kind of init we have. init.sh or init.py 
PWD=`pwd`
echo "current dir $PWD"
mkdir /opt
cp -r /opt /opt

echo "set handle sigterm/ sigkill"
_term() { 
  echo "Caught SIGTERM signal! stop cohorte" 
  echo "stop 0" -n | /bin/nc localhost 9001
}

trap _term SIGTERM

echo "check launch_jvm.sh exists"
if [ -f /opt/node/launch/launch_cohorte.sh ]; then
	echo "launch launch_cohorte.sh "
	echo "start cohorte" 
	sh /opt/node/launch/launch_cohorte.sh
else
	echo "no file /opt/node/launch/launch_cohorte.sh"
	ls /opt/node/launch/

fi

#/usr/lib/systemd/systemd --system
