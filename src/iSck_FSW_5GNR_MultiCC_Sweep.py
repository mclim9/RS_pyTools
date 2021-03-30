""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Main Code
# #############################################################################
numCC = 4
freq_arry = [24e9, 28e9, 39e9, 43e9]
delta = 99.96e6
mode = 'AUTO'                           # AUTO | SING
pwr_strt = -20
pwr_stop = 0
pwr_step = 1

fileOut = open(f'{__file__}.txt', 'a')
FSW = iSocket().open('192.168.58.109', 5025)
FSW.s.settimeout(15)
fileOut.write(f'{FSW.idn}\n')
SMW = iSocket().open('192.168.58.114', 5025)
fileOut.write(f'{SMW.idn}\n')
fileOut.write('Mode,Freq,Pwr,EVM1,EVM2,EVM3,EVM4\n')

FSW.write('INIT:CONT OFF')
for freq in freq_arry:
    FSW.write(f':SENS:FREQ:CENT:CC1 {freq - (delta * 1.5)}')
    FSW.write(f':SENS:FREQ:CENT:CC2 {freq - (delta * 0.5)}')
    FSW.write(f':SENS:FREQ:CENT:CC3 {freq + (delta * 0.5)}')
    FSW.write(f':SENS:FREQ:CENT:CC4 {freq + (delta * 1.5)}')
    SMW.write(f':SOUR:FREQ:CW {freq}')
    SMW.query(':SOUR1:CORR:FRES:RF:OPT:LOC;*OPC?')
    for pwr in range(pwr_strt, pwr_stop, pwr_step):
        SMW.write(f'SOUR:POW:LEV:IMM:AMPL {pwr}')
        FSW.write('INIT:CONT ON')
        FSW.write(f':CONF:NR5G:CSC AUTO')
        FSW.query(':SENS:ADJ:LEV;*OPC?')
        FSW.write(f':CONF:NR5G:CSC {mode}')
        FSW.write('INIT:CONT OFF')
        FSW.query('INIT:IMM;*OPC?')
        EVM1 = FSW.query(':FETC:CC1:SUMM:EVM:ALL:AVER?')
        EVM2 = FSW.query(':FETC:CC2:SUMM:EVM:ALL:AVER?')
        EVM3 = FSW.query(':FETC:CC3:SUMM:EVM:ALL:AVER?')
        EVM4 = FSW.query(':FETC:CC4:SUMM:EVM:ALL:AVER?')
        data = f'{mode},{freq},{pwr},{EVM1},{EVM2},{EVM3},{EVM4}'
        print(data)
        fileOut = open(f'{__file__}.txt', 'a')
        fileOut.write(f'{data}\n')
        fileOut.close()
