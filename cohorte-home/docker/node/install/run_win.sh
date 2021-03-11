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

echo "check launch_jvm.sh exists"
if [ -f /c/opt/node/felix/launch/launch_jvm_win.sh ]; then
	echo "launch launch_jvm.sh "
	echo "start cohorte" 
	
	bash /c/opt/node/felix/launch/launch_jvm_win.sh
	echo "finish started"
	
else
	echo "no file /c/opt/node/felix/launch/launch_jvm_win.sh"
	ls /c/opt/node/felix/launch/
fi
