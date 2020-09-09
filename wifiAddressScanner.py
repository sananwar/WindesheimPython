from subprocess import Popen, PIPE
import subprocess
import re
import os
from sense_hat import SenseHat

macRegex = re.compile(r"(?:[0-9a-fA-F]:?){12}")
ipAddressRegex = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")

addresses = []
red = (255, 0, 0)
green = (0, 255, 0)

def getNetworkAddres():
    ips = os.popen("ip addr show wlan0")
    for ip in ips:
    	rat = re.findall(ipAddressRegex,ip)
    	if len(rat) > 1:
    		return(rat[0])

macAdresses = ["98:09:cf:8c:e9:d9", "60:45:cb:86:23:73"]
networkAdress = getNetworkAddres()

sh = SenseHat()
#Searches in arp cache file for certain macaddresses
def searchIpWithMac():
    pids = os.popen("arp -a")
    for pid in pids:
        deviceName = pid.split()[0]
        mac = re.findall(macRegex,pid)
        ipAddress = re.findall(ipAddressRegex,pid)

        if(len(mac) > 0 and mac[0] in macAdresses):
            #print(deviceName, mac, ipAddress)
            addresses.append(ipAddress[0])
            sh.clear(green)

#scans the network and add found devices to the arp cache file
def scanNetwork():
    with open(os.devnull, "wb") as limbo:
        for n in range(1, 255):
                ip=networkAdress.format(n)
                result=subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2", ip],
                        stdout=limbo, stderr=limbo).wait()
                if result:
                        print(ip, "inactive")
                else:
                        print (ip, "active")

def checkIfIpStillOnline():
    print(addresses)
    for adres in addresses:
        res = subprocess.call(['ping', '-c', '3', adres])
        if res == 0:
            print("ping to", adres, "OK")
            sh.clear(green)
        elif res == 2:
            print("no response from", adres)
            scanNetwork()
        else:
            print("ping to", adres, "failed!")
            scanNetwork()
            sh.clear(red)
#scanNetwork()

#searchIpWithMac()
#checkIfIpStillOnline()
