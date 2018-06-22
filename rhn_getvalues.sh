#!/bin/sh
#
# Pablo Iranzo Gómez (Pablo.Iranzo@gmail.com)
#
# Script for getting custom info values for a system
#

. $RHNUTILS_PATH/rhn_common.sh

python $RHNUTILS_PATH/rhn_getvalues.py -u $RHN_USER -p $RHN_PASS -s https://$RHN_SERVER/rpc/api
