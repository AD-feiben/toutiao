#!/bin/sh

python3=`which python3 | awk '{print $1}'`

if [ -z "${python3}" ]; then
	echo "Not install Python3"
else
	virtualenv -p ${python3} venv
fi

exit 0 

