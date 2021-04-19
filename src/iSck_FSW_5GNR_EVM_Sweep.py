""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module
from iSck_FSW_5GNR_GetSettings import get_5GNR_settings

# #############################################################################
# ## Main Code
# #############################################################################
freq_arry = [36e9, 39e9, 43e9, 44e9, 47e9, 50e9]
freq_arry = range(int(36e9), int(50e9), int(1e9))
pwr_arry = range(-50, 5, 1)
# freq_arry = range(int(46e9), int(47e9), int(50e6))
# pwr_arry = [-10, -8, -6, -4, -2]
filename = __file__.split('.py')[0] + '.txt'

fileOut = open(filename, 'a')
FSW = iSocket().open('169.254.58.109', 5025)
FSW.s.settimeout(15)
fileOut.write(f'{FSW.idn}\n')
SMW = iSocket().open('169.254.58.114', 5025)
fileOut.write(f'{SMW.idn}\n')
fileOut.write(f'{get_5GNR_settings()}\n')
fileOut.write('Mode,Freq,Power [dBm],EVM [dB],Gen\n')

FSW.write('INIT:CONT OFF')
FSW.write(':SENS:NR5G:FRAM:COUN:AUTO OFF')
FSW.write(':SENS:NR5G:FRAM:COUN 1')
for mode in ['EVM']:
    for freq in freq_arry:
        FSW.write(f':SENS:FREQ:CENT {freq}')
        SMW.write(f':SOUR:FREQ:CW {freq}')
        SMW.query(':SOUR1:CORR:FRES:RF:OPT:LOC;*OPC?')
        for pwr in pwr_arry:
            SMW.write(f'SOUR:POW:LEV:IMM:AMPL {pwr}')
            FSW.write('INIT:CONT ON')
            FSW.query(f':SENS:ADJ:{mode};*OPC?')
            FSW.write('INIT:CONT OFF')
            FSW.query('INIT:IMM;*OPC?')
            EVM = FSW.query(':FETC:CC1:SUMM:EVM:ALL:AVER?')
            data = f'{mode},{freq},{pwr},{EVM},FE50DTR'
            print(data)
            fileOut = open(filename, 'a')
            fileOut.write(f'{data}\n')
            fileOut.close()
