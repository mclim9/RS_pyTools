"""Rohde & Schwarz Automation for IQ Analyzer use."""
from iSocket import iSocket                                         # Import socket module
import timeit

def VSA_Basic():
    # s.write(':INST:CRE:NEW SANALYZER, "Spectrum"')
    s.write(':INST:SEL "Spectrum"')             # Select Spectrum
    s.write(':INIT:CONT OFF')                   # Continuous Off
    s.write(f':SENS:FREQ:STAR {FStart}')        # Stop Freq
    s.write(f':SENS:FREQ:STOP {FStop}')         # Star Freq
    s.write(':SENS:BAND:RES:AUTO ON')           # RBW Auto
    s.write(':SENS:BAND:VID:AUTO ON')           # VBW Auto
    s.write(':INP:ATT:AUTO ON')                 # Attn Auto
    s.write(':DISP:Y:RLEV 0 ')                  # Ref Level

def Calc_Test_Time(numSteps):
    tick = timeit.default_timer()
    s.query('INIT:IMM;*OPC?')
    timeDelta = timeit.default_timer() - tick
    # swpTime   = float(s.query(':SENS:SWE:TIME?'))
    testTime = numSteps * timeDelta
    print(f'Single point take {timeDelta:7.4f} sec * {numSteps:.0f}')
    print(f'Estimated test time: {testTime:7.2f} sec')
    print(f'                or : {testTime/60:7.2f} min')
    print(f'                or : {testTime/3600:7.2f} Hours')
    return timeDelta

def Spur_Search():
    VSA_Basic()
    s.write(':CALC1:MARK1:STAT ON')
    s.write(':CALC1:MARK1:FUNC:BPOW:STAT ON')
    s.write(':CALC1:MARK1:FUNC:BPOW:SPAN 120000')

    loopStart = int(FStart + FStep)
    loopStop  = int(FStop - FStep)
    loopStep  = int(FStep)
    loopNum   = (loopStop - loopStart) / loopStep
    Calc_Test_Time(loopNum)
    for freq in range(loopStart, loopStop, loopStep):
        s.write(f':CALC1:MARK1:X {freq}')
        s.query('INIT:IMM;*OPC?')
        MkrPwr = s.query('CALC:MARK:FUNC:BPOW:RES?')
        MkrPwr = float(MkrPwr)
        # print(f'Pwr at {freq} is {MkrPwr:7.3f}')

if __name__ == "__main__":
    s      = iSocket().open('192.168.58.109', 5025)
    FStart = 5e9
    FStop  = 5.1e9
    FStep  = 120e3
    Spur_Search()
