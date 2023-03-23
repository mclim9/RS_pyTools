"""R&S Example code"""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Code Begin
# #############################################################################
SMW = iSocket().open('192.168.58.114', 5025)
FSW = iSocket().open('192.168.58.109', 5025)

freq = 3.45e9

FSW.write(f':SENS:FREQ:CENT {freq}')                # FSW Center freq
FSW.write('INIT:CONT OFF')                          # FSW Single Sweep
FSW.write(f':SENS:FREQ:SPAN 10e6')                  # FSW Span
FSW.write(':SENS:SWE:TIME 0.0005')                  # FSW sweep time
SMW.write(f':SOUR1:FREQ:CW {freq}')                 # SMW Center Freq
SMW.write('SOUR1:POW:LEV -10')                      # SMW RMS Power
SMW.write('OUTP1:STAT 1')                           # SMW Power ON

print('Freq  , RMS,Amplit,FSW-Mkr')
for RMSPwr in range(-80, 5, 5):
    SMW.write(f'POW {RMSPwr}')                              # SMW Power
    FSW.query('INIT:IMM;*OPC?')                             # FSW Single Sweep
    FSW.write('CALC1:MARK1:MAX:PEAK')                       # FSW Marker Peak Search
    mkr = FSW.queryFloat(':CALC1:MARK1:Y?')                 # FSW Marker dBm Value
    FSW.write(f':DISP:WIND:TRAC:Y:SCAL:RLEV {mkr + 10}')    # FSW Adjust Ref Level
    FSW.query('INIT:IMM;*OPC?')                             # FSW Single Sweep
    mkr = FSW.queryFloat(':CALC1:MARK1:Y?')                 # FSW Marker Peak Search
    outStr = f'{freq/1e9:6.3f},{RMSPwr:4d},{mkr:6.2f}'      # Print results
    print(outStr)
