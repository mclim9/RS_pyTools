"""Rohde & Schwarz Automation for demonstration use. """
# BS 1-H
from iSocket import iSocket                                 # Import socket module

def config_SEM(freq, BW):
    # s.write(':INST:SEL "5G NR"')
    freq_list = [-500, -300, -200, -140, -120, -110, -104, -100, 100, 105, 120, 140, 200, 300, 500]

    # s.query(':CONF:NR5G:MEAS ESP;*OPC?')
    # s.write(f':SENS:ESP1:RANG7:INS AFT')                      # Insert Range after Range7 (throw away)
    # s.write(f':SENS:ESP1:RANG1:INS BEF')                      # Insert Range before Range1 (throw away)

    s.write(f':SENS:FREQ:SPAN 1GHZ')
    s.write(f':SENS:ESP1:RANG1:FREQ:STAR {freq_list[0]}')       # Range1 Start
    freq_list.pop(0)
    for i, limit in enumerate(freq_list):
        s.write(f':SENS:ESP1:RANG{i+1}:FREQ:STOP {limit}MHZ')   # Range1 Stop
        s.write(f':SENS:ESP1:RANG{i+2}:FREQ:STAR {limit}MHz')   # Range2 Start

if __name__ == "__main__":
    s = iSocket().open('172.24.225.128', 5025)
    # config_SEM(3500e6, 100)
    config_SEM(3550e6, 100)
    s.clear_error()
