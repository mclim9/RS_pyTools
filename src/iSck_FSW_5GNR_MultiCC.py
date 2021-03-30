""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Main Code
# #############################################################################
numCC = 4
freq  = 28e9
delta = 99.96e6
FSW = iSocket().open('192.168.58.109', 5025)

FSW.write(f':CONF:NR5G:NOCC {numCC}')       # Set numCC
FSW.write(f':SENS:FREQ:CENT:CC1 {freq - (delta * 1.5)}')
FSW.write(f':SENS:FREQ:CENT:CC2 {freq - (delta * 0.5)}')
FSW.write(f':SENS:FREQ:CENT:CC3 {freq + (delta * 0.5)}')
FSW.write(f':SENS:FREQ:CENT:CC4 {freq + (delta * 1.5)}')
