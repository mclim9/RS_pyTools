""" Rohde & Schwarz demonstration code"""
from iSocket import iSocket

# #############################################################################
# ## Main Code
# #############################################################################
s = iSocket().open('192.168.58.109', 5025)

ChSpan = 10e6
numAvg = 50

# #############################################################################
# ## Common Setup
# #############################################################################
s.write(':SENS:FREQ:SPAN 20e6')                         # Set Span
s.write('SWE:POIN 1001')                                # Sweep Points
s.write(':DISP:TRAC:Y:RLEV -40')                        # Reference Level
s.write(':INP:ATT 0')                                   # Attenuation
s.write(':INP:GAIN:STAT ON')                            # Preamp ON
s.write(':SENS:WIND1:DET1:FUNC POS')                    # Positive Peak Dtctr
s.write(':DISP:TRAC:MODE AVER')                         # Averaging On
s.write(':SENS:AVER:TYPE POW')                          # Averaging Type
s.write(f':SWE:COUN {numAvg}')                          # Number of averages
s.write(':SENS:SWE:TIME:AUTO ON')                       # Sweep Time Auto
s.write(':INIT:CONT OFF')


# #############################################################################
# ## Channel Pwr Setup
# #############################################################################
s.write(':SENS:BAND:RES 100e3')                         # RBW
s.write(':SENS:BAND:VID 1e6')                           # VBW
s.write(':SENS:AVER:TYPE LOG')                          # Averaging Type
freqArry = [635e6, 737e6, 751e6, 847e6, 942.5e6, 1575.4e6, 1842e6, 1960e6, 2140e6, 2442e6, 2655e6, 5320e6]
for freq in freqArry:
    s.write(f':SENS:FREQ:CENT {freq}')                  # Set Center Frequency

    s.write(':CALC1:MARK1:FUNC:BPOW:STAT ON')           # Marker Ch power on
    s.write(f':CALC1:MARK1:FUNC:BPOW:SPAN {ChSpan}')    # Marker Ch power span
    s.write(f':CALC1:MARK1:X {freq}')                   # Set Marker1 Frequency
    s.query(':INIT:IMM;*OPC?')
    chPwr = s.query(':CALC1:MARK1:FUNC:BPOW:RES?')      # Channel Power

    print(f'ChPwr  : {freq} {chPwr} dBm/{ChSpan}')

# #############################################################################
# ## Spot Power Setup
# #############################################################################
freqArry = [797e6, 1066.5e6, 1864e6, 2128e6, 2392e6, 2661.5e6, 5318e6, 5587.5e6]
s.write(':SENS:BAND:RES 10e3')                      # RBW
s.write(':SENS:BAND:VID 10e3')                      # VBW
s.write(':SENS:AVER:TYPE POW')                      # Averaging Type
s.write(':SENS:FREQ:SPAN 5e6')                      # Set Span
for freq in freqArry:
    s.write(f':SENS:FREQ:CENT {freq}')              # Set Center Frequency

    s.write(f':CALC1:MARK2:X {freq}')               # Set Marker Frequency
    s.write(':CALC1:MARK2:FUNC:NOIS:STAT ON')       # Marker PSD measure
    s.query(':INIT:IMM;*OPC?')
    PSD = s.query(':CALC2:MARK1:FUNC:NOIS:RES?')    # PSD results
    print(f'SpotPwr: {freq} {PSD} dBm/Hz')
