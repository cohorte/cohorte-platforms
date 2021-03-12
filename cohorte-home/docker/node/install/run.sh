#!/bin/bash
echo "--- Boot of Cohorte Container..."
#./opt/init.sh
# check what kind of init we have. init.sh or init.py 
PWD=`pwd`
echo "current dir $PWD"
whoami

echo "set handle sigterm/ sigkill"
_term() { 
  echo "Caught SIGTERM signal! stop cohorte" 
  echo "stop 0" -n | /bin/nc localhost 9001
}

trap _term SIGTERM

if [ -f /opt/init.sh ]; then
	sh /opt/init.sh
fi

# execute shell 
echo "execute dependencies if we need a new dependency in the docker container"
for deps in init_container_*.sh ; do
	echo "call sh $deps $*"
	sh $deps $*
done

echo "run python init_container_*.py $*"
# for all init container call by alphabetical order in
for init in init_container_*.py ; do
	echo "call python3 $init $* "
	python3 $init $*
done
echo "check launch_jvm.sh exists"
if [ -f /opt/node/felix/launch/launch_jvm.sh ]; then
	echo "launch launch_jvm.sh "
	echo "start cohorte" 
	dos2unix  /opt/node/felix/launch/launch_jvm.sh
	dos2unix  /opt/node/felix/launch/config.properties
	
	bash /opt/node/felix/launch/launch_jvm.sh
	echo "finish started"
	
else
	echo "no file /c/opt/node/felix/launch/launch_jvm.sh"
	ls /opt/node/felix/launch/
fi
