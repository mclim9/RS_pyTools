""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Main Code
# #############################################################################
FSW = iSocket().open('192.168.58.109', 5025)
Span = 5e6
FSW.write(':INST:SEL "SPECTRUM"')           # Select Analog Demod
FSW.write(':INIT:CONT OFF')                 # Single Sweep
FSW.write(':SENS:FREQ:CENT 6.6GHz')
FSW.write(f':SENS:FREQ:SPAN {Span}')
print(f' RBW|  Pts |Hz/Pt| Stat|Freq      | MkrPwr')
for rbw in [1000, 5000]:
    for pts in [1001, 5001, 10001]:
        FSW.write(f':SENS:BAND:RES {rbw}')
        FSW.write(f':SENS:SWE:POIN {pts}')
        FSW.query('INIT:IMM;*OPC?')
        FSW.write(':CALC1:MARK1:MAX:PEAK')
        frq = FSW.query(':CALC1:MARK1:X?')
        pwr = FSW.queryFloat(':CALC1:MARK1:Y?')
        ptDist = Span/pts
        if rbw - ptDist > 0:
            stat = 'good'
        else:
            stat = 'bad '
        print(f'{rbw}|{pts:6d}|{ptDist:5.0f}| {stat}|{frq}|{pwr:7.2f}')