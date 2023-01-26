"""Rohde & Schwarz Automation for demonstration use. """
# BS 1-H
from iSocket import iSocket                                 # Import socket module

def config_SEM(freq, BW):
    # s.write(':INST:SEL "5G NR"')
    band_min_freq = 3260000000
    band_max_freq = 3840000000
    SEM_lower     = band_min_freq - freq
    SEM_upper     = band_max_freq - freq

    s.query(':CONF:NR5G:MEAS ESP;*OPC?')
    s.write(f':SENS:FREQ:CENT {freq}')
    s.write(f':CONF:NR5G:DL:CC1:DFR LOW')                   # Freq Range: MIDD | LOW
    s.write(f':CONF:NR5G:BST FR1H')                         # BS 1-H
    s.write(f':CONF:NR5G:DL:CC1:BW BW5')                    # Reset limits
    s.write(f':CONF:NR5G:DL:CC1:BW BW{BW}')                 # Configure BW (resets upper and lower limits)
    s.write(':SENS:ESP1:SSET 0')                            # Symetrical Setup off
    s.write(f':SENS:ESP1:RANG7:INS AFT')                    # Insert Range after Range7 (throw away)
    s.write(f':SENS:ESP1:RANG1:INS BEF')                    # Insert Range before Range1 (throw away)
    # Carrier is always __range 5__

    if abs(SEM_upper) > abs(SEM_lower):
        print('Upper Limit Larger')                         # Upper limit larger
        s.write(f':SENS:FREQ:SPAN {2 * SEM_upper}')         # Enlarge Span as needed
        s.write(f':SENS:ESP1:RANG1:FREQ:STAR {-SEM_upper}') # Range1 Start (throw away)
        s.write(f':SENS:ESP1:RANG2:FREQ:STAR {SEM_lower}')  # Range2 Stop
        s.write(f':SENS:ESP1:RANG8:FREQ:STOP {SEM_upper}')  # Range8 Stop
    else:
        print('Lower larger')                               # Lower limit larger
        s.write(f':SENS:FREQ:SPAN {-2 * SEM_lower}')        # Enlarge Span as needed
        s.write(f':SENS:ESP1:RANG2:FREQ:STAR {SEM_lower}')  # Range1 Start
        s.write(f':SENS:ESP1:RANG8:FREQ:STOP {SEM_upper}')  # Range7 Stop
        s.write(f':SENS:ESP1:RANG9:FREQ:STOP {-SEM_lower}') # Range8 Stop (throw away)

if __name__ == "__main__":
    s = iSocket().open('192.168.58.109', 5025)
    # config_SEM(3500e6, 100)
    config_SEM(3550e6, 100)
    s.clear_error()
