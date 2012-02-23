#!/bin/bash
#
# Pablo Iranzo Gómez (Pablo.Iranzo@redhat.com)
#
# Sample script for populating some values using auxiliary scripts
#
#

if [ -f /etc/sysconfig/rhn/systemid ]
then
	#Get hardware identification
	TIPO=$(dmidecode |grep "Product Name:"|grep "[0-9].*"|head -n 1|cut -d ":" -f 2|tr -d " [:cntrl:]")

	case $TIPO in
		Dell)
			hardware="laptop"
			$RHNUTILS_PATH/rhn_setname.sh "`echo $(hostname).c$CENTRO`";;
		*)
			hardware="Server";;
	esac
	$RHNUTILS_PATH/rhn_setgroup.sh "$hardware"
	$RHNUTILS_PATH/rhn_setgroup.sh "$TIPO"
	
	$RHNUTILS_PATH/rhn_addnote.sh "Valores updated" "grupos"
fi