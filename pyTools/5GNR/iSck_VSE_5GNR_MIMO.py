""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Main Code
# #############################################################################
VSE = iSocket().open('127.0.0.1', 5025)
VSE = iSocket().open('192.168.58.109', 5025)
VSE.timeout(10)

IDN = VSE.query('*IDN?')
# print(VSE.query('DEV:LIST?'))
for slot in range(2):
    for alloc in (0, 1):
        VSE.write(f'CONF:NR5G:DL:CC1:FRAM1:BWP0:SLOT{slot}:ALL{alloc}:CLM LC21')
for error in range(3):
    print(VSE.query('SYST:ERR?'))
