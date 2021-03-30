""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module
# from a_textLog import testLog                # textLog

# #############################################################################
# ## Main Code
# #############################################################################
freq_arry = [1.9e9, 2.4e9, 3.5e9]
pwr_arry = range(-30, 5, 1)
filename = __file__.split('.py')[0] + '.txt'

fileOut = open(filename, 'a')
FSW = iSocket().open('192.168.58.109', 5025)
FSW.s.settimeout(15)
fileOut.write(f'{FSW.idn}\n')
SMW = iSocket().open('192.168.58.114', 5025)
fileOut.write(f'{SMW.idn}\n')
fileOut.write('Mode,Freq,Power [dBm],EVM [dB]\n')

FSW.write('INIT:CONT OFF')
FSW.write(':SENS:NR5G:FRAM:COUN:AUTO OFF')
FSW.write(':SENS:NR5G:FRAM:COUN 1')
for mode in ['EVM', 'LEV']:
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
            data = f'{mode},{freq},{pwr},{EVM}'
            print(data)
            fileOut = open(filename, 'a')
            fileOut.write(f'{data}\n')
            fileOut.close()
