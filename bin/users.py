#!/usr/bin/env python

# shows users

from tools.logs import log, logging
from tools.bash import route, nmap, nbtscan, ifconfig
import socket
import os
import sys

def getUsers():
    """ prints list of ip, MAC, hardware, netbios """

    log.info("listing users")
    
    # get data
    router = route().router
    subnet =  router +  "/24"
    nmap1 = nmap("-sn -n %s" % subnet)
    nbtscan1 = nbtscan(subnet)
    ifconfig1 = ifconfig()
    
    # add current machine
    nmap1.ip.add(ifconfig1.wlanip)
    nmap1.mac[ifconfig1.wlanip] = ifconfig1.wlanmac
    nbtscan1.netbios[ifconfig1.wlanip] = "** this pc **"

    # flag router
    nbtscan1.netbios[router] = "** router **"

    # print formatted
    try:
        nmap1.ip = sorted(nmap1.ip, key=lambda item: socket.inet_aton(item))
    except:
        log.error("Problem sorting ip addresses")
    format1 = '{0:<15} {1:<17} {2:<15} {3:<15}'
    print(format1.format("ip", "mac", "hardware", "netbios"))
    print(format1.format("==", "===", "========", "======="))
    for ip in nmap1.ip:
        print(format1.format(ip, nmap1.mac.get(ip, ""), nmap1.hw.get(ip,""), nbtscan1.netbios.get(ip, "")))

log.setLevel(logging.INFO)
getUsers()