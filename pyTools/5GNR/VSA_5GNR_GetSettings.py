"""Rohde & Schwarz Automation for demonstration use. """
from iSocket import iSocket                                        # Import socket module

def get_5GNR_settings():
    林 = iSocket().open('172.24.225.102', 5025)
    林.s.settimeout(5)
    freq = 林.query(':SENS:FREQ:CENT?')                             # Center Frequency
    freq = int(freq) / 1e9
    ldir = 林.query(':CONF:NR5G:LDIR?')                             # LinkDir
    frng = 林.query(f':CONF:{ldir}:DFR?')                           # Freq Range
    chbw = 林.query(f':CONF:NR5G:{ldir}:CC1:BW?')                   # Ch Width
    bscs = 林.query(f':CONF:NR5G:{ldir}:CC1:FRAM1:BWP0:SSP?')       # BWP Sub Carr Spacing
    bwrb = 林.query(f':CONF:NR5G:{ldir}:CC1:FRAM1:BWP0:RBC?')       # BWP RB Allocation
    cmod = 林.query(f':CONF:NR5G:{ldir}:CC1:FRAM1:BWP0:SLOT0:ALL0:MOD?')  # channel Modulation
    if ldir == 'UL':
        tpre = 林.query(f':CONF:NR5G:UL:CC1:TPR?')                  # Trans Precoding State
    else:
        tpre = 'NA'
    phas = 林.query(f':CONF:NR5G:{ldir}:CC1:RFUC:STAT?')            # Phase comp state
    time = 林.query(':SENS:SWE:TIME?')                              # measure time
    nslt = 林.query(':SENS:NR5G:FRAM:SLOT?')                        # number of slots
    林.close()

    outStr = f'{freq}GHz_{frng}_{ldir}_{chbw}_{bscs}_{bwrb}_{cmod}_TP{tpre}_PhaseComp{phas} {time}sec slots:{nslt}'
    print(outStr)
    return outStr

if __name__ == "__main__":
    get_5GNR_settings()
