""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Main Code
# #############################################################################
VSE = iSocket().open('127.0.0.1', 5025)
VSE.timeout(10)

IDN = VSE.query('*IDN?')
VSE.write('INST:BLOC:CHAN:SOUR FILE')        # DEV or FILE
VSE.write('INST:BLOC:CHAN:DEV "FSW-43*"')   # Select instrument
VSE.write(':INIT:CONT OFF')
VSE.query(':INIT:IMM;*OPC?')
print(VSE.query('SYST:ERR?'))
print(VSE.query('SYST:ERR?'))
