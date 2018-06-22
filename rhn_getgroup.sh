#!/bin/sh
#
# Pablo Iranzo Gómez (Pablo.Iranzo@gmail.com)
#
# Description: Script for obtaining groupmembership for this host
#

. $RHNUTILS_PATH/rhn_common.sh

SERVER=`cat /etc/sysconfig/rhn/up2date|grep serverURL=|cut -d "/" -f 3`
python $RHNUTILS_PATH/rhn_getgroup.py -u $RHN_USER -p $RHN_PASS -s https://$RHN_SERVER/rpc/api
