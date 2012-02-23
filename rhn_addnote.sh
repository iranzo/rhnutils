#!/bin/sh
#
# Pablo Iranzo Gómez (Pablo.Iranzo@redhat.com)
#
# Script for adding notes to Satellite profile

. $RHNUTILS_PATH/rhn_common.sh

if [ "$1" == "" ]
then
	echo Usage: $0 VAR VALUE
else
	if [ "$2" == "" ]
	then
		 echo Usage: $0 VAR VALUE
	else
		python $RHNUTILS_PATH/rhn_addnote.py -u $RHN_USER -p $RHN_PASS -n "$1" -v "$2" -s https://$RHN_SERVER/rpc/api
	fi
fi

