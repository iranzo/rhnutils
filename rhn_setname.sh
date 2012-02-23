#!/bin/sh
#
# Pablo Iranzo Gómez (Pablo.Iranzo@redhat.com)
#
# Script for setting profilename in satellite

. $RHNUTILS_PATH/rhn_common.sh

if [ "$1" == "" ]
then
	echo Usage: $0 VAR VALUE
else
	python $RHNUTILS_PATH/rhn_setname.py -u $RHN_USER -p $RHN_PASS -n $1 -s https://$RHN_SERVER/rpc/api
fi

