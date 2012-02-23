#!/bin/sh
#
# Pablo Iranzo Gómez (Pablo.Iranzo@redhat.com)
#
# Script for obtaining a reactivation key for this profile to keep history, groups, events, etc
#

. $RHNUTILS_PATH/rhn_common.sh

python $RHNUTILS_PATH/rhn_reactiva.py -u $RHN_USER -p $RHN_PASS -s https://$RHN_SERVER/rpc/api
