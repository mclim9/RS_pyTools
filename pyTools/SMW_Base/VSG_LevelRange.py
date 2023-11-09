""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

SMW = iSocket().open('192.168.58.114', 5025)

for freq in range(1000000000, 44000000000, 500000000):
    for pwr in [0]:
        SMW.write(f':SOUR1:FREQ:CW {freq}')
        SMW.query(f':SOUR1:POW:LEV {pwr};*OPC?')
        pwrL = SMW.queryFloat(f':OUTP:AFIX:RANG:LOW?')
        pwrU = SMW.queryFloat(f':OUTP:AFIX:RANG:UPP?')
        print(f'{freq},Hz, {pwr},dbm, {pwrL:6.2f}, {pwrU:6.2f}')
