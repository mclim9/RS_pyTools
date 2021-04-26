""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Main Code
# #############################################################################
FSW = iSocket().open('192.168.58.109', 5025)
FSW.s.settimeout(5)
data = FSW.query(':TRAC4:DATA? TRACE1').split(',')
for i, dat in enumerate(data):
    print(f'{dat:7s} ', end='')
    if i % 9 == 8:
        print('')
print(len(data))
