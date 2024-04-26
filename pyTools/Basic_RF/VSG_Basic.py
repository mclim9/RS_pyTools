""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module


def Config_VSG():
SMW = iSocket().open('192.168.58.115', 5025)

SMW.write(f':SOUR1:FREQ:CW 12e9')           # Center Frequency
SMW.query(f':SOUR1:POW:LEV -10;*OPC?')      # RMS Power Level
SMW.write(f':SOUR1:POW:LEV:IMM:OFFS 0')     # Power Offset
SMW.write(f':SOUR1:IQ:STAT 0')              # IQ Modulation OFF
SMW.write(f':OUTP1:STAT 1')                 # RF ON

def Config_VSA():
    FSW = iSocket().open('192.168.58.109', 5025)
    freq   = 1e9

    FSW.write(':INST:SEL "Analog Demod"')       # Select Analog Demod
    FSW.write(':INIT:CONT OFF')                 # Single Sweep
    FSW.write(':DISP:WIND1:SUBW:TRAC:Y:SCAL:PDIV 200e6')
    FSW.write(':SENS:BWID:DEM 200e6')
    FSW.write(f':SENS:FREQ:CENT {freq}')        # Center Freq
    FSW.write(':CALC1:MARK1:STAT ON')           # Window1 Marker1 ON
    FSW.write(':CALC1:MARK2:STAT ON')           # Window1 Marker2 ON
    for i in range(100):
        FSW.write(':INIT:IMM;*OPC?')
        mkr1 = FSW.query(':CALC1:MARK1:Y?')
        mkr2 = FSW.query(':CALC1:MARK2:Y?')
        print(f'Marker1:{mkr1} Marker2:{mkr2}')

