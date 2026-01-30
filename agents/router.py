#!/usr/bin/env python3
import sys
cmd = ' '.join(sys.argv[1:]).lower()
if cmd.startswith('ledger'):
    print('→ Routed to Ledger')
elif cmd.startswith('atlas'):
    print('→ Routed to Atlas')
elif cmd.startswith('forge'):
    print('→ Routed to Forge')
else:
    print('No agent matched')