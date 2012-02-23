#!/bin/sh
#
# Pablo Iranzo Gómez (Pablo.Iranzo@redhat.com)
#
# Common values for the remaining scripts to interact with RHN/Satellite API

RHN_SERVER=`cat /etc/sysconfig/rhn/up2date|grep serverURL=|cut -d "/" -f 3`
RHN_USER=custom
RHN_PASS=custom
RHNUTILS_PATH=/root/scripts

export RHN_SERVER RHN_USER RHN_PASS
