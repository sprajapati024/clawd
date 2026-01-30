"""Finance categorization"""
from common import log_tokens

def run(transactions):
    out=[]
    for t in transactions:
        log_tokens('mistral',10)
        out.append({**t,'category':'other'})
    return out

if __name__=='__main__': print(run([{'desc':'Store','amt':10}]))
