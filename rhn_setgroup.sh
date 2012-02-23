#!/bin/sh
#
# Pablo Iranzo Gómez (Pablo.Iranzo@redhat.com)
#
# Script for adding system to a group and create that group if it doesn't exists 
#

. $RHNUTILS_PATH/rhn_common.sh

if [ "$1" == "" ]
then
	echo Usage: $0 GRUPO
else
	python $RHNUTILS_PATH/rhn_setgroup.py -u $RHN_USER -p $RHN_PASS -n $1 -s https://$RHN_SERVER/rpc/api
fi

