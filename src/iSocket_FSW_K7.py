""" Rohde & Schwarz Automation for demonstration use."""
# pylint: disable=E0611,E0401,invalid-name
from iSocket import iSocket             # Import socket module

# #########################################################
# ## Main Code
# #########################################################
FSW = iSocket().sOpen('192.168.58.109', 5025)

FSW.sWrite(':INST:SEL "Analog Demod"')      # Select Analog Demod
FSW.sWrite(':INIT:CONT OFF')                # Single Sweep
FSW.sWrite(':DISP:WIND1:SUBW:TRAC:Y:SCAL:PDIV 200e6')
FSW.sWrite(':SENS:BWID:DEM 200e6')
FSW.sWrite(':CALC1:MARK1:STAT ON')          # Window1 Marker1 ON
FSW.sWrite(':CALC1:MARK2:STAT ON')          # Window1 Marker2 ON
for i in range(10000):
    FSW.sWrite(':INIT:IMM;*OPC?')
    mkr1 = FSW.sQuery(':CALC1:MARK1:Y?')
    mkr2 = FSW.sQuery(':CALC1:MARK2:Y?')
    print(f'Marker1:{mkr1} Marker2:{mkr2}')
