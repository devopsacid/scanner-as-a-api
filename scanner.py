#!/usr/bin/env python3
# Port Scanner for analyses of network and opened ports
# Utilize python-nmap library
#
# Contact: Michal Maxian - michal@maxian.sk
# Date: 20.7.2023

# Usage in docker:
# docker run -it --rm -v ./data:/data --name scanner-cli scanner-cli 192.168.100.26
# data directory have to be in current directory

import os
import sys
import nmap
import json
from jsondiff import diff

# Function to scan IP list
def scaniplist(ip):
    scanner=nmap.PortScanner()
    scanner.scan(ip,'1-1024','-v --version-all')
    hosts=scanner.all_hosts()
    return scanner

def scanip(ip):
    scanner=nmap.PortScanner()
    scanner.scan(ip,'1-1024','-v --version-all')
    hosts=scanner.all_hosts()
    result=[]
    for host in hosts:
        state=scanner[host].state()
        if state=="up":
            # append host to result json
            result.append(scanner[host])
    return json.dumps(result)

# Function to load json from file
def loadjson(filename):
    with open(filename,"r") as f:
        json=f.read()
        f.close()
    return json

# Function to write json to file
def writejson(filename,json):
    with open(filename,"w") as f:
        f.write(json)
        f.close()

# Function to print scan results
def print_scan_results(scanner,host):
    # print all protocols and ports in humnan readable format
    protocols=scanner[host].all_protocols()
    for prot in protocols:
        ports=scanner[host][prot].keys()
        for port in ports:
            port_state=scanner[host][prot][port]
            print(f" {prot} {port}")

def main():
    # Directory for storing scan results /data
    # Have to be mounted to container
    scandir=os.environ.get('SCANDIR') if os.environ.get('SCANDIR') else "/data"
    if not os.path.exists(scandir):
        print(f"Directory {scandir} does not exists, please create it and mount to container")
        exit(1)

    if len(sys.argv) < 1: 
        print(f"Usage: ")
        print(f"\t{sys.argv[0]} IP")
        print(f"\n\tIP could be simple IP or IP range in format 192.168.1.1-10")
        exit(1)
    else:
        ip=sys.argv[1]

    scan=scaniplist(ip)
    hosts=scan.all_hosts()

    for host in hosts:
        state=scan[host].state()
        filename=f"{scandir}/{host}"

        # if host is up, print it and scan it and compare with old diff
        if state=="up":
            print(f"{host}: {state}")

            # Check if file exists and if yes, compare with old scan
            if os.path.exists(filename):
                # read old scan from file 
                jsonold=loadjson(filename)
                jsondiff=diff(jsonold,json.dumps(scan[host]), marshal=True) # compare diff with old scan
                if not jsondiff=={}:
                    print(f"old scan found, diff is: {jsondiff}")
            # write new scan to file as json
            writejson(filename,json.dumps(scan[host]))

            # print all protocols and ports in humnan readable format
            print_scan_results(scan,host)
    return 0
