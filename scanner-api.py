#!/usr/bin/env python3
# Port Scanner API for analyses of network and opened ports
# Utilize python-nmap library
#
# Contact: Michal Maxian
# Date: 21.7.2023

import os
import sys
import redis
import json
from jsondiff import diff
from scanner import scanip, scaniplist
from flask import Flask, jsonify, request

app = Flask(__name__)

### FUNCTIONS ###
def store_to_redis(host, data):
    for i, value in enumerate(data):
        field = f"field{i}"
        redis_conn.hset(host, field, json.dumps(value))
        print(f"STORE TO REDIS host output KEY: {host} {value}")
        sys.stdout.flush()

def load_from_redis(ip):
    redis_results = redis_conn.hgetall(ip)
    if redis_results:
        return {field.decode(): value.decode() for field, value in redis_results.items()}
    else:
        print(f"IP {ip} not found in Redis")
        sys.stdout.flush()
        return {}

def scan_diff(ip):
    scan_results = scanip(ip)
    redis_results = load_from_redis(ip)

    if not redis_results:
        print(f"IP {ip} not found in Redis")
        sys.stdout.flush()
        return {}

    results = diff(redis_results, scan_results, marshal=True)
    return results

def redis_listall(redis_conn): 
    redis_results = redis_conn.keys('*')
    keys = [key.decode('utf-8') for key in redis_results]
    print(f"REDIS KEYS: {keys}")
    sys.stdout.flush()
    return jsonify(keys), 200

def cleandb(redis_conn):  
    redis_conn.flushdb()
    return jsonify({'status': 'OK'}), 200

### ROUTES ###
@app.route('/scan', methods=['GET'])
def scan_endpoint():
    ip_address = request.args.get('ip', None)
    if ip_address is None:
        return jsonify({'error': 'No IP address provided'}), 400
    scan_data = scaniplist(ip_address)
    json_data = []
    for host in scan_data.all_hosts():
        state=scan_data[host].state()
        print(f"HOST: {host} STATE: {state}")
        if state == "up":
            print(f"STORE TO REDIS host output KEY: {host} {scan_data[host]}")
            json_data.append(scan_data[host])
            store_to_redis(host,scan_data[host])

    results = json.dumps(json_data) 
    print(f"SCAN RESULT FOR {host}: {results}")
    sys.stdout.flush()
    return jsonify(results), 200

@app.route('/scandiff', methods=['GET'])
def scan_diff_endpoint():
    ip_address = request.args.get('ip', None)
    if ip_address is None:
        return jsonify({'error': 'No IP address provided'}), 400
    scan_data = scaniplist(ip_address)
    json_data = []
    diff_data = []
    for host in scan_data.all_hosts():
        state=scan_data[host].state()
        print(f"HOST: {host} STATE: {state}")
        if state == "up":
            print(f"STORE TO REDIS host output KEY: {host} {scan_data[host]}")
            json_data.append(scan_data[host])
            diff_data.append(scan_diff(host))
            store_to_redis(host,scan_data[host])

    results = json.dumps(diff_data) 
    print(f"SCAN DIFF RESULT FOR {host}: {results}")
    sys.stdout.flush()
    return jsonify(results), 200

@app.route('/health', methods=['GET'])
def health_endpoint():
    return jsonify({'status': 'OK'}), 200

@app.route('/listscans', methods=['GET'])
def listscans():
    return redis_listall(redis_conn)

@app.route('/cleandb', methods=['GET'])
def clean_db():
    return cleandb(redis_conn)

### MAIN ###
if __name__ == '__main__':
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
    REDIS_DB = os.environ.get('REDIS_DB', 0)
    try:
        redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        if redis_conn.ping(): 
            print(f'Connected to Redis {REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}')
            sys.stdout.flush()
        else:
            print(f'Unable to ping Redis {REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}')
            sys.stdout.flush()
            exit(1)
    except redis.ConnectionError:
        print(f'Unable to connect to Redis {REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}')
        sys.stdout.flush()
        exit(1)

    app.run(host='0.0.0.0', port=8000, debug=True)
    