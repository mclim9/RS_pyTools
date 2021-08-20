""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Main Code
# #############################################################################
FSW = iSocket().open('192.168.58.109', 5025)
Freq = 37e9
Num_CC = 4
Freq_Delta = 99.96e6
Freq_Off = Freq + (-Num_CC/2 - 0.5) * Freq_Delta
Samp = 491.52e6

FSW.write(':INST:SEL "IQ Analyzer"')        # Select Analog Demod
FSW.write(f':SENS:FREQ:CENT {Freq}')        # Center Frequency
FSW.write(f':TRAC:IQ:SRAT {Samp}')          # Sampling Rate
FSW.write(':SENS:SWE:TIME 0.01')            # Capture time

for i in range(1,Num_CC+1):
    FSW.write(f'CALC1:MARK{i}:STAT ON')
    FSW.write(f'CALC1:MARK{i}:FUNC:BPOW:STAT ON')
    FSW.write(f'CALC1:MARK{i}:FUNC:BPOW:SPAN 95.04e6')
    FSW.write(f'CALC1:MARK{i}:X {Freq_Off + Freq_Delta*i}')
