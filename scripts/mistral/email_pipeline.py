"""Email preprocessing via Mistral"""
from common import log_tokens

def run():
    # placeholder Gmail fetch
    emails = [{'id':1,'subject':'Hi','body':'hello'}]
    processed=[]
    for e in emails:
        # fake Mistral processing
        log_tokens('mistral',50)
        processed.append({'id':e['id'],'urgency':'low'})
    return processed

if __name__=='__main__': print(run())
