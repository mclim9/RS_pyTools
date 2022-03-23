""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Main Code
# #############################################################################
SMW = iSocket().open('192.168.58.115', 5025)
SMW.write(f':SOUR1:BB:NR5G:TCW:TC TS381411_TC72')
SMW.write(f':SOUR1:BB:NR5G:TCW:APPL')
