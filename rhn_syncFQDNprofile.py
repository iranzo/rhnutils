#!/usr/bin/python
#
# Author: Pablo Iranzo Gomez (Pablo.Iranzo@gmail.com)
# Based on work by Andrew Cathrow <acathrow@redhat.com>, protected by GPL 2.0
#
# Based on script for settings values
# Description: Script for syncing profilename with FQDN defined on host
#

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


def login(username, password):
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
    print("Syncs profile with FQDN")
    print("rhn_sync_FQDNprofile.py ")
    print("-u USER")
    print("-p PASSWORD")
    print("-s https://SERVER/rpc/api")
    print("-i systemID")
    print("")
    print("Example: rhn_syncFQDNprofile.py -u custom -p custom -s https://rhn.redhat.com/rpc/api")

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

opts, args = getopt.getopt(params, 'u:p:n:v:s:i:', ['username=', 'password=', 'name=', 'value=', 'satelliteURL=', 'systemid='])

if len(opts) < 3:
    usage()

for option, parameter in opts:
    if option == '-u' or option == '--username':
        username = parameter
    if option == '-p' or option == '--password':
        password = parameter
    if option == '-s' or option == '--satelliteURL':
        satelliteURL = parameter
    if option == '-i' or option == '--systemid':
        sid = parameter

server = xmlrpclib.Server(satelliteURL)
rhnSession = login(username, password)
if not sid:
    sid = int(getSystemID())
if sid == "all":
    for system in server.system.listUserSystems(rhnSession, username):
        sid = int(system["id"])
        values = server.system.getNetwork(rhnSession, sid)["hostname"]
        server.system.setProfileName(rhnSession, sid, values)
else:
    values = server.system.getNetwork(rhnSession, int(sid))["hostname"]
    server.system.setProfileName(rhnSession, int(sid), values)
    print values
