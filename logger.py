import json
log = []

def add(timestamp, data):
    log.append((timestamp, data))

def save():
    with open('log.txt', 'w') as f:
        f.write(json.dumps(log))
