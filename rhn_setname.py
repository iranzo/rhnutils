#!/usr/bin/python
#
# Author: Pablo Iranzo Gomez (Pablo.Iranzo@gmail.com)
# Based on work by Andrew Cathrow <acathrow@redhat.com>, protected by GPL 2.0
#
# Based on script for settings values
# Description: Script for altering displayname on satellite for this host

import getopt
import os
import re
import sys
import xmlrpclib


# Server URL
# 	Replace with your Satellite's URL
satelliteURL = ''

sysid = '/etc/sysconfig/rhn/systemid'

username = ''
password = ''
name = ''
val = ''


def login(username, password):
    rhnSession = None
    try:
        rhnSession = server.auth.login(username, password)
    except xmlrpclib.Fault, fault:
        if fault.faultCode == -20:
            rhnlogin(username, password)
        else:
            print("Error logging on")
            sys.exit(1)
    return rhnSession


def usage():
    print("Sets CUSTOM_INFO values for Satellite from command line")
    print("rhn_setname.py ")
    print("-u USER")
    print("-p PASSWORD")
    print("-n VAR")
    print("-s https://SERVER/rpc/api")
    print("")
    print("Example: rhn_setname.py -u custom -p custom -n PROFILENAME -s https://rhn.redhat.com/rpc/api")

    sys.exit(1)


def getSystemID():
    if not os.path.isfile(sysid):
        print("Unable to open System ID file")
        print("Is the system registered ?")
        sys.exit(2)

    f = open(sysid, 'r')
    output = False
    for l in f.readlines():
        reg = re.compile("ID-(\d+)")
        if reg.search(l):
            output = reg.search(l).group(1)
    f.close()
    if not output:
        print("Unable to retrieve system id")
        sys.exit(3)
    return output

params = sys.argv[1:]

opts, args = getopt.getopt(params, 'u:p:n:s:', ['username=', 'password=', 'name=', 'satelliteURL='])

if len(opts) != 4:
    usage()

for option, parameter in opts:
    if option == '-u' or option == '--username':
        username = parameter
    if option == '-p' or option == '--password':
        password = parameter
    if option == '-n' or option == '--name':
        name = parameter
    if option == '-s' or option == '--satelliteURL':
        satelliteURL = parameter

server = xmlrpclib.Server(satelliteURL)
rhnSession = login(username, password)
sid = int(getSystemID())
server.system.setProfileName(rhnSession, sid, name)
