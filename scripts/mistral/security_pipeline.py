"""Security log analysis"""
from common import log_tokens

def run():
    alerts=[]
    with open('/var/log/auth.log','r',errors='ignore') as f:
        for line in f:
            if 'Failed password' in line:
                log_tokens('mistral',5)
                alerts.append(line.strip())
    return alerts

if __name__=='__main__': print(run())
