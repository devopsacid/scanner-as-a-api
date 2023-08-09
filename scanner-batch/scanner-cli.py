#!/usr/bin/env python3
# Port Scanner batch runner for scheduled runs
# Utilize scanner-as-a-service API
#
# Contact: Michal Maxian
# Date: 25.7.2023

import os
import requests
import time
import sys

def getscan(scanner_endpoint, ip):
    params = {'ip': ip}
    response = requests.get(scanner_endpoint, params=params)
    if response.status_code != 200:
        print(f"ERROR: {response.status_code} {response.reason}", file=sys.stdout)
        exit(1)
    return response.json()

def main():
    sys.stdout.flush()
    SCANNER_URL = os.environ.get('SCAN_ENDPOINT', 'localhost')
    SCANNER_PORT = os.environ.get('SCAN_PORT', '8000')
    SCAN_IP = os.environ.get('SCAN_IP', 'localhost')
    SCAN_FUNCTION = os.environ.get('SCAN_FUNCTION', 'scan')
    SCAN_INTERVAL = int(os.environ.get('SCAN_INTERVAL', '300'))
    SCANNER_ENDPOINT = f"http://{SCANNER_URL}:{SCANNER_PORT}/{SCAN_FUNCTION}"
    print(f"Starting scanner batch job for endpoint: {SCANNER_ENDPOINT}", file=sys.stdout)
    print(f"Scan IP: {SCAN_IP}", file=sys.stdout)
    print(f"Scan interval: {SCAN_INTERVAL} seconds", file=sys.stdout)

    while True:
        print(f"Starting scan for IP: {SCAN_IP}", file=sys.stdout)
        scan = getscan(SCANNER_ENDPOINT, SCAN_IP)
        print(f"SCAN IP: {SCAN_IP} METHOD: {SCAN_FUNCTION} RESULT: {scan}", file=sys.stdout)
        sys.stdout.flush()
        time.sleep(SCAN_INTERVAL)

print("Starting scanner cli...")
main()
exit(0)
