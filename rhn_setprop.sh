#!/bin/sh
#
# Pablo Iranzo Gómez (Pablo.Iranzo@gmail.com)
#
# Script for editing custom_info values for being used with configuration files 'Macros' or scripts
#

. $RHNUTILS_PATH/rhn_common.sh

if [ "$1" == "" ]
then
	echo Usage: $0 VAR VALUE
else
	if [ "$2" == "" ]
	then
		 echo Usage: $0 VAR VALUE
	else
		python $RHNUTILS_PATH/rhn_setprop.py -u $RHN_USER -p $RHN_PASS -n $1 -v $2 -s https://$RHN_SERVER/rpc/api
	fi
fi

