#!/bin/bash
echo "--- Boot of Cohorte Container..."
#./opt/init.sh
# check what kind of init we have. init.sh or init.py 
PWD=`pwd`
echo "current dir $PWD"
cd /opt

if [ -f /opt/node/felix/launch/launch_jvm.sh ]; then
	sh /opt/node/felix/launch/launch_jvm.sh
fi

# execute shell 
echo "execute dependencies if we need a new dependency in the docker container"
for deps in init_container_*.sh ; do
	echo "call sh $deps $*"
	sh $deps $*
done


echo "set handle sigterm/ sigkill"
_term() { 
  echo "Caught SIGTERM signal! stop cohorte" 
  /bin/echo "stop 0" -n | /bin/nc localhost 9001
}

trap _term SIGTERM

echo "start cohorte" 
#/usr/lib/systemd/systemd --system
