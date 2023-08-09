# Brief documentation for scanner-batch.py

## Purpose
Get response from scanner-as-a-service API 
Run regular scans in interval.

## scanner-cli.py
You can launch scanner-cli from command line with command (see example):  
`SCAN_ENDPOINT=10.152.183.23 SCAN_IP=192.168.1.1 python3 scanner-cli.py`

## Configuration
You can set values in `scanner-batch-deployment.yml`
```yaml 
env:
- name: SCAN_ENDPOINT
    value: "scanner-api-service"
- name: SCAN_PORT
    value: "8000"
- name: SCAN_IP
    value: "192.168.1.1"    # replace with IP you want to scan
- name: SCAN_FUNCTION
    value: "scan"           # methods could be scan or scandiff
- name: SCAN_INTERVAL
    value: "300"            # give a value in seconds for the interval between scans
```

## Howto run
use Makefile with commands:  
  `make build` - build docker image  
  `make push` - push to dockerhub  
  `make deploy` - deploy to microk8s  
  `make clean` - delete from microk8s  
  `make redeploy` - clean build push deploy for quick redeployment
