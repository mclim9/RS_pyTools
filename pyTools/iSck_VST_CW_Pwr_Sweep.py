"""R&S Example code"""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Code Begin
# #############################################################################
SMW = iSocket().open('192.168.58.114', 5025)
FSW = iSocket().open('192.168.58.109', 5025)

freq = 3.45e9
# f = open(fileName, 'rb')
# data    = f.read()
# f.close()

FSW.write(f':SENS:FREQ:CENT {freq}')
FSW.write('INIT:CONT OFF')
FSW.write(f':SENS:FREQ:SPAN 10e6')
FSW.write(':SENS:SWE:TIME 0.0005')
SMW.write(f':SOUR1:FREQ:CW {freq}')
SMW.write('SOUR1:POW:LEV -10')
SMW.write('OUTP1:STAT 1')

print('Freq  , RMS,Amplit,Offst,ucorr ,FSW-Mkr, RMS + ucorr - off - mkr')
for RMSPwr in range(-80, 5, 5):
    SMW.write(f'POW {RMSPwr}')
    ampli = SMW.queryFloat(f':SOUR1:POW:POW?')
    offst = SMW.queryFloat(f'SOUR1:POW:LEV:IMM:OFFS?')
    ucorr = SMW.queryFloat(f'SOUR1:CORR:VAL?')
    FSW.query('INIT:IMM;*OPC?')
    FSW.write('CALC1:MARK1:MAX:PEAK')
    mkr = FSW.queryFloat(':CALC1:MARK1:Y?')
    FSW.write(f':DISP:WIND:TRAC:Y:SCAL:RLEV {mkr + 10}')
    FSW.query('INIT:IMM;*OPC?')
    mkr = FSW.queryFloat(':CALC1:MARK1:Y?')
    outStr = f'{freq/1e9:6.3f},{RMSPwr:4d},{ampli:6.2f},{offst:5.2f},{ucorr:6.2f}, {mkr:6.2f}, {RMSPwr+ucorr-offst-mkr:6.2f}'
    print(outStr)
