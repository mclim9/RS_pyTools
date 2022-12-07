""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Main Code
# #############################################################################
FSW = iSocket().open('192.168.58.109', 5025)
FSW.timeout(5)

f = open(__file__.split('.')[0] + '.txt', 'wb')
# FSW.write(':INST:SEL "Spectrum"')           # Select Analog Demod
FSW.write(':INIT:CONT OFF')                 # Single Sweep

pathIQ = 0
if pathIQ:
    FSW.write('FORM REAL,32')               # ASCII Output
    dataY = FSW.queryBin('TRAC1:DATA? TRACE1')
    dataX = FSW.queryBin('TRAC1:DATA:X? TRACE1')
    f.write(dataY)
else:
    FSW.write('FORM ASCII')                 # ASCII Output
    dataY = FSW.query('TRAC1:DATA? TRACE1')
    dataX = FSW.query('TRAC1:DATA:X? TRACE1')
    f.write(dataY.encode())


f.close()
