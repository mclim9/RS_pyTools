""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Main Code
# #############################################################################
VSE = iSocket().open('127.0.0.1', 5025)
VSE.timeout(10)

IDN = VSE.query('*IDN?')
# print(VSE.query('DEV:LIST?'))
VSE.write('INST:BLOC:CHAN:SOUR DEV')        # DEV or FILE
VSE.write('INST:BLOC:CHAN:DEV "FSW-43*"')   # Select instrument
VSE.write('INST:BLOC:CHAN:SOUR:TYPE "RF"')  # Instrument
VSE.write(':INIT:CONT OFF')
VSE.query(':INIT:IMM;*OPC?')
VSE.query('INST:BLOC:CHAN:DEV?')
print(VSE.query('SYST:ERR?'))
print(VSE.query('SYST:ERR?'))
