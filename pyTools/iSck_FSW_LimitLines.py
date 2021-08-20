""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Main Code
# #############################################################################
FSW = iSocket().open('192.168.58.109', 5025)

limit_name = 'Upper_Lim'
limit_Freq = 150000
FSW.write(f':CALC:LIM:NAME "{limit_name}"')     # Limit Name
FSW.write(':CALC:LIM:CONT:DOM TIME')            # X Units
FSW.write(':CALC:LIM:CONT:MODE ABS')            # X Scaling
FSW.write(':CALC:LIM:CONT:SPAC LIN')            # X Spacing
FSW.write(':CALC:LIM:CONT:DATA 64e-6,400e-6')   # X Values
FSW.write(':CALC:LIM:UNIT HZ')                  # Y Units
FSW.write(':CALC:LIM:UPP:SPAC LIN')             # Y Spacing
FSW.write(f':CALC:LIM:UPP:DATA {limit_Freq},{limit_Freq}')   # Y Values Upper
FSW.write(f':CALC1:LIM1:NAME "{limit_name}"')   # Select Limit
FSW.write(':CALC1:LIM1:TRAC1:CHEC ON')          # Limit Check ON
FSW.write(':CALC1:LIM1:STAT ON')                # Limit Visible ON

limit_name = 'Lower_Lim'
FSW.write(f':CALC:LIM:NAME "{limit_name}"')     # Limit Name
FSW.write(':CALC:LIM:CONT:DOM TIME')            # X Units
FSW.write(':CALC:LIM:CONT:MODE ABS')            # X Scaling
FSW.write(':CALC:LIM:CONT:SPAC LIN')            # X Spacing
FSW.write(':CALC:LIM:CONT:DATA 64e-6,400e-6')    # X Values
FSW.write(':CALC:LIM:UNIT HZ')                  # Y Units
FSW.write(':CALC:LIM:LOW:SPAC LIN')             # Y Spacing
FSW.write(f':CALC:LIM:LOW:DATA -{limit_Freq},-{limit_Freq}')   # Y Values Lower
FSW.write(':CALC1:LIM1:TRAC1:CHEC ON')          # Limit Check ON
FSW.write(':CALC1:LIM1:STAT ON')                # Limit Visible ON
