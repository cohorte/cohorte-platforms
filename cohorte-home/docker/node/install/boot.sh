#!/bin/bash
echo "--- Boot of Cohorte Container..."
#./opt/init.sh
# check what kind of init we have. init.sh or init.py 
PWD=`pwd`
echo "current dir $PWD"
cd /opt

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


exec /usr/sbin/init
#/usr/lib/systemd/systemd --system
