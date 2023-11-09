"""Rohde & Schwarz Automation for demonstration use. """
# BS 1-H
from iSocket import iSocket                                 # Import socket module

def config_SEM(freq, BW):
    # s.write(':INST:SEL "5G NR"')
    # s.query(':CONF:NR5G:MEAS ESP;*OPC?')
    s.write(f':SENS:FREQ:CENT {freq}')
    s.write(f':CONF:NR5G:DL:CC1:DFR LOW')                   # Freq Range: MIDD | LOW
    s.write(f':CONF:NR5G:BST FR1H')                         # BS 1-H
    s.write(f':CONF:NR5G:DL:CC1:BW BW{BW}')
    # s.write(f':SENS:FREQ:SPAN {span}')                    # Enlarge Span as needed

    range = []
    range.append(s.queryFloat(':SENS:ESP1:RANG1:FREQ:STAR?') / 1e6)  # Range1 Start
    range.append(s.queryFloat(':SENS:ESP1:RANG1:FREQ:STOP?') / 1e6)  # Range1 Stop
    range.append(s.queryFloat(':SENS:ESP1:RANG1:LIM1:ABS:STAR?'))    # Range1 Limit Start

    range.append(s.queryFloat(':SENS:ESP1:RANG2:FREQ:STAR?') / 1e6)  # Range2 Start
    range.append(s.queryFloat(':SENS:ESP1:RANG2:FREQ:STOP?') / 1e6)  # Range2 Stop
    range.append(s.queryFloat(':SENS:ESP1:RANG2:LIM1:ABS:STAR?'))    # Range2 Limit Start

    range.append(s.queryFloat(':SENS:ESP1:RANG3:FREQ:STAR?') / 1e6)  # Range3 Start
    range.append(s.queryFloat(':SENS:ESP1:RANG3:FREQ:STOP?') / 1e6)  # Range3 Stop
    range.append(s.queryFloat(':SENS:ESP1:RANG3:LIM1:ABS:STAR?'))    # Range3 Limit Start

    range.append(s.queryFloat(':SENS:ESP1:RANG4:FREQ:STAR?') / 1e6)  # Range4 Start
    range.append(s.queryFloat(':SENS:ESP1:RANG4:FREQ:STOP?') / 1e6)  # Range4 Stop

    range.append(s.queryFloat(':SENS:ESP1:RANG5:FREQ:STAR?') / 1e6)  # Range5 Start
    range.append(s.queryFloat(':SENS:ESP1:RANG5:FREQ:STOP?') / 1e6)  # Range5 Stop
    range.append(s.queryFloat(':SENS:ESP1:RANG5:LIM1:ABS:STAR?'))    # Range5 Limit Start

    range.append(s.queryFloat(':SENS:ESP1:RANG6:FREQ:STAR?') / 1e6)  # Range6 Start
    range.append(s.queryFloat(':SENS:ESP1:RANG6:FREQ:STOP?') / 1e6)  # Range6 Stop
    range.append(s.queryFloat(':SENS:ESP1:RANG6:LIM1:ABS:STAR?'))    # Range6 Limit Start

    range.append(s.queryFloat(':SENS:ESP1:RANG7:FREQ:STAR?') / 1e6)  # Range7 Start
    range.append(s.queryFloat(':SENS:ESP1:RANG7:FREQ:STOP?') / 1e6)  # Range7 Stop
    range.append(s.queryFloat(':SENS:ESP1:RANG7:LIM1:ABS:STAR?'))    # Range7 Limit Start
    print(range)

if __name__ == "__main__":
    s = iSocket().open('192.168.58.109', 5025)
    config_SEM(25e9, 20)
    s.clear_error()
