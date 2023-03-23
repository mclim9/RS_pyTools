"""R&S Example code"""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Code Begin
# #############################################################################
SMW = iSocket().open('192.168.58.114', 5025)
FSW = iSocket().open('192.168.58.109', 5025)

freq = 3.45e9

FSW.write(f':SENS:FREQ:CENT {freq}')                # FSW Center freq
SMW.write(f':SOUR1:FREQ:CW {freq}')                 # SMW Center Freq
