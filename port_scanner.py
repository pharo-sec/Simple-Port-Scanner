#!/usr/bin/env python3
import socket
import subprocess
import sys
import argparse
from termcolor import colored
from datetime import datetime

openPorts = []

# A function that expands ranges seperated with a '-'
def expandRange(ports):
    final = []
    for i in ports.split(','):
        if '-' not in i:
            final.append(int(i))
        else:
            l,h = map(int, i.split('-'))
            final+= range(l,h+1)
    return final

parser = argparse.ArgumentParser(description='A Port Scanning Tool')
parser.add_argument("-t", "--target_host", help="The target to be scanned", default= "127.0.0.1")
parser.add_argument("-p", "--port_scan", help="Port scan options", default= "0-65535")
args = parser.parse_args()
remoteServer = args.target_host
portRange = args.port_scan

portScan = expandRange(portRange)

# Clear the screen
subprocess.call('clear', shell=True)

# Get host IP if it's a domain name
remoteServerIP  = socket.gethostbyname(remoteServer)

# Print a nice banner with information on which host we are about to scan
print ("-" * 60)
print ("Please wait, scanning remote host", remoteServerIP)
print ("-" * 60)

# Check scan start time
t1 = datetime.now()

try:
    for port in portScan:  
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServerIP, port))
        if result == 0:
            print ("[+] Port {}:    Open".format(port))
            openPorts.append(port)
        sock.close()

except KeyboardInterrupt:
    print ("You pressed Ctrl+C")
    sys.exit()

except socket.gaierror:
    print ('Hostname could not be resolved. Exiting')
    sys.exit()

except socket.error:
    print ("Couldn't connect to server")
    sys.exit()

# Get scan completion time
t2 = datetime.now()

# Calculate the difference of time
total =  t2 - t1

# Printing the information to screen
print ('Scanning Completed in: ', total)
