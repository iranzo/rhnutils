#!/bin/bash
# 
# Description: clone-tree is a script based on spacecmd which recursively
# copies a tree of channels to another name using a based channel name
# structure.  This eases the maintenance of staging trees for development,
# integration and production and its associated subchannels
#
# Requires: Spacecmd package installed and operating, must be run from Satellite server
#
# Author: Alfredo Moralejo (Alfredo.Moralejo@redhat.com)
# Modified by: Francisco Lloreda (flloreda@redhat.com)
# Modified by: Pablo Iranzo Gómez (Pablo.Iranzo@gmail.com)
#
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

if [ "$1" == "" ];
then
	echo "Usage $0 source_channel destination_prefix destination_suffix user password"
	echo ""
	echo "Example: $0 int-customer-rhel-x86_64-server-5 des 5_6 SATUID SATPASS"
	echo "            Will copy int-customer-rhel-x86_64-server-5 and its subchannels to a new structure"
	echo "            named like des-customer-rhel-x86_64-server-5_6 and replacing description with 5_6 in the line"
	echo ""
	exit 0
fi

SRCBASECHN=$1
DESTPREFIX=$2
DESTSUFIX=$3
USER=$4
PASSWORD=$5


SRCPREFIX=$( echo $SRCBASECHN|awk -F"-" '{print $1}')
SRCPREFIX_U=$( echo $SRCPREFIX | tr '[a-z]' '[A-Z]')
SRCSUFIX=$( echo $SRCBASECHN|rev|awk -F"-" '{print $1}'|rev)

DESTPREFIX_U=$( echo $DESTPREFIX | tr '[a-z]' '[A-Z]')

echo "Source Prefix=$SRCPREFIX"
echo "Source Sufix=$SRCSUFIX"

if [ $(spacecmd -u $USER -p $PASSWORD -- softwarechannel_listbasechannels | grep -c -w $SRCBASECHN ) -eq 0 ]
then
	echo "ERROR: Channel $SRCBASECHN is not a base channel"
	exit 1
fi


function get_channel_desc()
{

BASE=$1

DESC=$( echo $BASE|cut -d\- -f2-)
DESC=$( echo $DESC|rev|cut -d\- -f2-|rev)
echo $DESC

}

# Clone Base channel

SRCBASE=$(get_channel_desc $SRCBASECHN)

DESTBASECHN="$DESTPREFIX"-"$SRCBASE"-"$DESTSUFIX"
SRCBASECHNNAME=$(spacewalk-report channels|grep -w $SRCBASECHN |awk -F"," '{print $2}')
DESTBASECHNNAME=$( echo $SRCBASECHNNAME | sed "s/"$SRCPREFIX_U"/"$DESTPREFIX_U"/g"|sed "s/"$SRCSUFIX"/"$DESTSUFIX"/g")

echo "Cloning channel $SRCBASECHN with name $SRCBASECHNNAME to $DESTBASECHN with name $DESTBASECHNNAME"

spacecmd -u $USER -p $PASSWORD -- softwarechannel_clone -s $SRCBASECHN -n \"$DESTBASECHNNAME\" -l $DESTBASECHN 

for i in `spacecmd -u $USER -p $PASSWORD softwarechannel_listchildchannels |grep "^$SRCPREFIX"|grep "$SRCSUFIX\$"`
do
	SRCCHILDCHN=$i
	SRCCHILD=$(get_channel_desc $SRCCHILDCHN)
	DESTCHILDCHN="$DESTPREFIX"-"$SRCCHILD"-"$DESTSUFIX"
	SRCCHILDCHNNAME=$(spacewalk-report channels|grep -w $SRCCHILDCHN |awk -F"," '{print $2}')
	DESTCHILDCHNNAME=$( echo $SRCCHILDCHNNAME | sed "s/"$SRCPREFIX_U"/"$DESTPREFIX_U"/g"|sed "s/"$SRCSUFIX"/"$DESTSUFIX"/g")
	echo "Cloning channel $SRCCHILDCHN with name $SRCCHILDCHNNAME to $DESTCHILDCHN with name $DESTCHILDCHNNAME"
	spacecmd -u $USER -p $PASSWORD -- softwarechannel_clone -s $SRCCHILDCHN  -n \"$DESTCHILDCHNNAME\" -l $DESTCHILDCHN -p $DESTBASECHN 
	
done


