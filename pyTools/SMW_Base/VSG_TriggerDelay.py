""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

SMW = iSocket().open('192.168.58.115', 5025)

for freq in range(int(10e6), int(2e9), int(10e6)):
    SMW.query(f':SOUR1:BB:ARB:CLOC {freq};*OPC?')
    ptime = SMW.query(f':SOUR1:BB:ARB:TRIG:PTIM?')
    ptime = ptime.replace('"', '').replace('s', '')
    print(f'{freq} {ptime}')
