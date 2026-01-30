"""Memory distillation"""
from common import log_tokens
import glob

def run():
    facts=[]
    for fn in glob.glob('/root/clawd/memory/*.md'):
        log_tokens('mistral',20)
        facts.append({'file':fn,'summary':'stub'})
    return facts

if __name__=='__main__': print(run())
