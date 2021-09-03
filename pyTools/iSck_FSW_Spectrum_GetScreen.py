""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Main Code
# #############################################################################
FSW = iSocket().open('192.168.58.109', 5025)
FSW.timeout(5)

FSW.write(':INST:SEL "Spectrum"')           # Select Analog Demod
FSW.write(':INIT:CONT OFF')                 # Single Sweep
FSW.write('FORM ASCII')                     # ASCII Output
dataY = FSW.query('TRAC1:DATA? TRACE1')
dataX = FSW.query('TRAC1:DATA:X? TRACE1')
