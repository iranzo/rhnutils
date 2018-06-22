#!/usr/bin/env python
#
# Description: Script to interact with RHN/Satellite API for checking local RPM's and
# associate corresponding packages existing into satellite into the desired
# channel. This script doesn't upload missing packages, just puts the one
# already on satellite in this channel.
#
# Intended usage is to create a channel for example with a RHEL 4.2 content
# based from files of a previous DVD image without having to duplicate disk
# usage on satellite side
#
# Author: Pablo Iranzo Gomez (Pablo.Iranzo@gmail.com)
#

import os
import sys
import glob
import optparse

import xmlrpclib
import rpm


p = optparse.OptionParser()

p.add_option("-f", "--file", dest="ficher", help="Read packages file specified", metavar="ficher")
p.add_option("-u", "--user", dest="username", help="Username to use", metavar="username")
p.add_option("-p", "--password", dest="password", help="Password to use", metavar="password")
p.add_option("-s", "--server", dest="server", help="Satellite to use", metavar="server")
p.add_option("-c", "--channel", dest="channel", help="Channel to put packages in", metavar="channel")
p.add_option("-a", "--arch", dest="arch", help="Arch for created channel", metavar="arch")
p.add_option("-S", "--showarch", action="store_false", help="Show valid arches", metavar="showarch")

(options, args) = p.parse_args()


def login(username, password):
    try:
        rhnSession = server.auth.login(username, password)
    except xmlrpclib.Fault, fault:
        if fault.faultCode == -20:
            rhnSession = rhnlogin(username, password)
        else:
            print("Error logging on")
            sys.exit(1)
    return rhnSession


def get_rpm_info(rpm_file):
    """Returns rpm information by querying a rpm"""
    ts = rpm.ts()
    fdno = os.open(rpm_file, os.O_RDONLY)
    try:
        hdr = ts.hdrFromFdno(fdno)
    except rpm.error:
        fdno = os.open(rpm_file, os.O_RDONLY)
        ts.setVSFlags(rpm._RPMVSF_NOSIGNATURES)
        hdr = ts.hdrFromFdno(fdno)
    os.close(fdno)
    return {'name': hdr[rpm.RPMTAG_NAME], 'version': hdr[rpm.RPMTAG_VERSION], 'package_release': hdr[rpm.RPMTAG_RELEASE], 'epoch': hdr[rpm.RPMTAG_EPOCH], 'arch': hdr[rpm.RPMTAG_ARCH]}


if options.username is None:
    print("We need username specified")
    sys.exit(1)
if options.password is None:
    print("We need password specified")
    sys.exit(1)
if options.server is None:
    print("We need server specified")
    sys.exit(1)

satelliteURL = "https://%s/rpc/api" % options.server
server = xmlrpclib.Server(satelliteURL)
rhnSession = login(options.username, options.password)

if options.showarch is not None:
    arcs = ""
    for arquitectura in server.channel.software.listArches(rhnSession):
        arcs = "%s %s" % (arcs, arquitectura["label"])
    print(arcs)
    sys.exit(0)
if options.channel is None:
    print("We need channel specified")
    sys.exit(1)

try:
    server.channel.software.getDetails(rhnSession, options.channel)  # Search for existing channel
except:
    try:
        # Channel creation
        server.channel.software.create(rhnSession, options.channel, options.channel, 'Custom channel by', options.arch,
                                       '')
    except:
        print("Problem creating channel %s" % options.channel)
        print("Need arch and channel name:")
        arcs = ""
        for arquitectura in server.channel.software.listArches(rhnSession):
            arcs = "%s %s" % (arcs, arquitectura["label"])
        print(arcs)
        sys.exit(1)

for fichero in glob.glob(options.ficher):
    datos = get_rpm_info(fichero)
    try:
        # Look for pkg and it's existing ID
        paquete = server.packages.findByNvrea(rhnSession, datos["name"], datos["version"], datos["package_release"], '',
                                              datos["arch"])["id"]
    except:
        print("Error while getting package information, probably, it's missing")
        sys.exit(1)
        # Intentaremos asociar el paquete
    try:
        server.channel.software.addPackages(rhnSession, options.channel, paquete)
    except:
        print("Problems linking package %s to channel %s" % (fichero, options.channel))
        sys.exit(1)
