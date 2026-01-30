import json, time

TOKEN_LOG = '/root/clawd/scripts/mistral/token_log.jsonl'

def log_tokens(model, tokens):
    rec = {'ts': time.time(), 'model': model, 'tokens': tokens}
    with open(TOKEN_LOG, 'a') as f:
        f.write(json.dumps(rec)+'\n')
