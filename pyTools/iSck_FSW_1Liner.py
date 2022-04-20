""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Main Code
# #############################################################################
FSW = iSocket().open('192.168.58.109', 5025)
FSW.s.settimeout(5)
data = FSW.query('SYST:DATE?')
print(data)
