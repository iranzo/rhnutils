#!/usr/bin/python
#
# Author: Pablo Iranzo Gomez (Pablo.Iranzo@gmail.com)
# Based on work by Andrew Cathrow <acathrow@redhat.com>, protected by GPL 2.0
#
# Based on script for settings values
# Description: Script for creating cobbler entries based on ip and mac to create reservations in DHCP
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
    print("Syncs profile with FQDN, mac and IP for DHCP")
    print("rhn_register-in-cobbler-ip-mac.py")
    print("-u USER")
    print("-p PASSWORD")
    print("-s https://SERVER/rpc/api")
    print("-i systemID")
    print("-r profile/role")
    print("")
    print("Example: rhn_register-in-cobbler-ip-mac.py -u custom -p custom -s https://rhn.redhat.com/rpc/api -r default")

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

opts, args = getopt.getopt(params, 'u:p:n:v:s:i:r:', ['username=', 'password=', 'name=', 'value=', 'satelliteURL=', 'systemid=', 'profile='])

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
    if option == '-r' or option == '--profile':
        profile = parameter

server = xmlrpclib.Server(satelliteURL)
rhnSession = login(username, password)
if not sid:
    sid = int(getSystemID())
if sid == "all":
    for system in server.system.listUserSystems(rhnSession, username):
        sid = int(system["id"])
        hostname = server.system.getNetwork(rhnSession, sid)["hostname"]
        ip = server.system.getNetwork(rhnSession, sid)["ip"]
        for device in server.system.getNetworkDevices(rhnSession, sid):
            if device["ip"] == ip:
                mac = device["hardware_address"]
        if hostname and ip and mac:
            # Remove previous profile if it existed
            command = 'NAME=$(cobbler system find  --mac=%s) && [ "$NAME" != "" ] && cobbler system remove --name=$NAME' % mac
            os.system(command)
            # Add the new profile
            command = "cobbler system add --name=%s --profile=%s --mac-address=%s --ip-address=%s --netboot-enabled no --interface eth0" % (hostname, profile, mac, ip)
            os.system(command)
        else:
            print "ERROR ", hostname, ip, mac


else:
    hostname = server.system.getNetwork(rhnSession, sid)["hostname"]
    ip = server.system.getNetwork(rhnSession, sid)["ip"]
    for device in server.system.getNetworkDevices(rhnSession, sid):
        if device["ip"] == ip:
            mac = device["hardware_address"]
    if hostname and ip and mac:
        # Remove previous profile if it existed
        command = 'NAME=$(cobbler system find  --mac=%s) && [ "$NAME" != "" ] && cobbler system remove --name=$NAME' % mac
        os.system(command)
        # Add the new profile
        command = "cobbler system add --name=%s --profile=%s --mac-address=%s --ip-address=%s --netboot-enabled no --interface eth0" % (hostname, profile, mac, ip)
        os.system(command)
