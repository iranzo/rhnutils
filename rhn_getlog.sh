#!/bin/sh
#
# Pablo Iranzo Gómez (Pablo.Iranzo@redhat.com)
#
# Description: Script for getting event log for a system
#

. $RHNUTILS_PATH/rhn_common.sh

python $RHNUTILS_PATH/rhn_getlog.py -u $RHN_USER -p $RHN_PASS -s https://$RHN_SERVER/rpc/api
