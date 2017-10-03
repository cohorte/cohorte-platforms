#!/bin/bash
echo "--- Boot of Cohorte Container..."
#./opt/init.sh
# check what kind of init we have. init.sh or init.py 

if[ -f ./opt/init.sh ]; then
	echo "run /opt/init.sh $@"
	sh ./opt/init.sh "$@"
elif [-f ./opt/init.py ]; then
	echo "run python /opt/init.py $@"

	python ./opt/init.py "$@"
fi 


./usr/lib/systemd/systemd --system
