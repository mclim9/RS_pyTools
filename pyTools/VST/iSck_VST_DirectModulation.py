"""R&S Example code"""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Code Begin
# #############################################################################
SMW = iSocket().open('192.168.58.114', 5025)
FSW = iSocket().open('192.168.58.109', 5025)

freq = 20e9
# f = open(fileName, 'rb')
# data    = f.read()
# f.close()

FSW.write(f':SENS:FREQ:CENT {freq}')
FSW.write('INIT:CONT OFF')
SMW.write(f':SOUR1:FREQ:CW {freq}')
SMW.write('SOUR1:POW:LEV -10')

for phaseNoise in [-70, -80, -90]:
    SMW.write(f':SOUR1:NOIS:PHAS:STAT ON')
    SMW.write(f':SOUR1:NOIS:PHAS:LEV1 {phaseNoise}')
    SMW.write(f':SOUR1:NOIS:PHAS:LEV2 {phaseNoise-10}')
    SMW.write(f':SOUR1:NOIS:PHAS:LEV3 -199')
    SMW.write(f':SOUR1:NOIS:PHAS:LEV4 -199')
    SMW.write(f':SOUR1:NOIS:PHAS:LEV5 -199')
    for dataRate in [1e6, 2e6, 5e6, 10e6, 200e6, 500e6, 100e6, 200e6, 500e6]:
        SMW.query(f':SOUR1:BB:DM:SRAT {dataRate};*OPC?')
        FSW.query(f':SENS:DDEM:SRAT {dataRate};*OPC?')
        FSW.query('INIT:IMM;*OPC?')
        FSW.query('INIT:IMM;*OPC?')
        EVM = FSW.query(':CALC2:MARK:FUNC:DDEM:STAT:EVM?')
        EVM = float(EVM)
        outStr = f'{phaseNoise},{dataRate:f},{EVM:.3f}'
        print(outStr)
