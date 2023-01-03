""" Rohde & Schwarz Automation for demonstration use."""
from token import OP
from iSocket import iSocket                 # Import socket module
import timeit

SMW = iSocket().open('192.168.58.114', 5025)

def parameterChange(OptEVM, HQMode):
    if OptEVM in (1,'1','ON'):
        SMW.write(f':SOUR1:CORR:OPT:EVM 1')          # Optimize EVM
    elif OptEVM in (0,'0','OFF'):
        SMW.write(f':SOUR1:CORR:OPT:EVM 0')          # Optimize EVM

    if HQMode in (1,'1','ON'):
        SMW.write(f':SOUR1:BB:IMP:OPT:MOD QHIG')     # High Quality mode
    elif OptEVM in (0,'0','OFF'):
        SMW.write(f':SOUR1:BB:IMP:OPT:MOD FAST')     # High Quality mode

    SMW.query(':SOUR1:FREQ:CW 24.2GHz;*OPC?')

    tick = timeit.default_timer()
    SMW.query(':SOUR1:FREQ:CW 24GHz;*OPC?')
    timeDelta = timeit.default_timer() - tick
    print(f'OptEVM-{OptEVM} HQ-{HQMode} Time: {timeDelta:.3f} sec')

    tick = timeit.default_timer()
    SMW.query(':SOUR1:FREQ:CW 24.2GHz;*OPC?')
    timeDelta = timeit.default_timer() - tick
    print(f'OptEVM-{OptEVM} HQ-{HQMode} Time: {timeDelta:.3f} sec')

parameterChange('OFF','OFF')
parameterChange('OFF','ON')
parameterChange('ON','OFF')
parameterChange('ON','ON')
