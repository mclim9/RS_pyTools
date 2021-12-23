""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Main Code
# #############################################################################
numCC = 10
freq  = 24e9
delta = 99.96e6
FSW = iSocket().open('192.168.58.114', 5025)

for i in range(numCC):
    FSW.write(f':CONF:NR5G:DL:CC{i+1}:FRAM1:BWP0:CSL 1')
    FSW.write(f':CONF:NR5G:DL:CC{i+1}:FRAM1:BWP0:SLOT0:ALC 1')
    FSW.write(f':CONF:NR5G:DL:CC{i+1}:FRAM1:BWP0:SLOT0:ALL0:CW:MOD QAM64')
    FSW.write(f':CONF:NR5G:DL:CC{i+1}:FRAM1:BWP0:SLOT0:ALL0:CCOD:IMCS 17')
