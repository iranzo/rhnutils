#!/usr/bin/python
#
# Author: Pablo Iranzo Gomez (Pablo.Iranzo@redhat.com)
# Based on work by Andrew Cathrow <acathrow@redhat.com>, protected by GPL 2.0
#
# Based on script for settings values
# Description: Script for creating /etc/hosts like with data from satellite
#

import getopt
import sys
import xmlrpclib


# Server URL
# 	Replace with your Satellite's URL
satelliteURL = ''
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
    print("outputs etc/hosts list for ip/hostnames from satellite")
    print("rhn_etchosts.py ")
    print("-u USER")
    print("-p PASSWORD")
    print("-s https://SERVER/rpc/api")
    print("--static path/to/file")
    print("")
    print("Example: rhn_etchosts.py -u custom -p custom -s https://rhn.redhat.com/rpc/api")

    sys.exit(1)


params = sys.argv[1:]
static = False
opts, args = getopt.getopt(params, 'u:p:n:v:s:i:', ['username=', 'password=', 'name=', 'value=', 'satelliteURL=', 'static='])

if len(opts) < 3:
    usage()

for option, parameter in opts:
    if option == '-u' or option == '--username':
        username = parameter
    if option == '-p' or option == '--password':
        password = parameter
    if option == '-s' or option == '--satelliteURL':
        satelliteURL = parameter
    if option == '--static':
        static = parameter


server = xmlrpclib.Server(satelliteURL)
rhnSession = login(username, password)

if static:
    print "\n### Init of static file\n"
    f = open(static, 'r')
    output = False
    for l in f.readlines():
        print(l.replace("\n", ""))

print "\n### print of dynamic list\n"
for system in server.system.listUserSystems(rhnSession, username):
    sid = int(system["id"])
    hostname, ip = server.system.getNetwork(rhnSession, sid)["hostname"], server.system.getNetwork(rhnSession, sid)["ip"]
    print "%s    %s" % (ip, hostname)
