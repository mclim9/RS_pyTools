""" Rohde & Schwarz Automation for demonstration use."""
import timeit
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Main Code
# #############################################################################
SMW = iSocket().open('192.168.58.114', 5025)
tick = timeit.default_timer()
SMW.write(f':SOUR1:BB:NR5G:TCW:TC TS381411_TC72')
SMW.query(f':SOUR1:BB:NR5G:TCW:APPL;*OPC?')
time = timeit.default_timer() - tick
print(f'CmdTime: {time} secs')
