"""Rohde & Schwarz Automation for demonstration use. """

from iSocket import iSocket                                         # Import socket module

# ##############################################################################
# ## Main Code
# ##############################################################################
def get_5GNR_settings():
    s = iSocket().open('192.168.58.105', 5025)
    freq = s.query(':SENS:FREQ:CENT?')                              # Center Frequency
    freq = int(freq) / 1e9
    ldir = s.query(':CONF:NR5G:LDIR?')                              # LinkDir
    frng = s.query(f':CONF:{ldir}:DFR?')                            # Freq Range
    chbw = s.query(f':CONF:NR5G:{ldir}:CC1:BW?')                    # Ch Width
    bscs = s.query(f':CONF:NR5G:{ldir}:CC1:FRAM1:BWP0:SSP?')        # BWP Sub Carr Spacing
    bwrb = s.query(f':CONF:NR5G:{ldir}:CC1:FRAM1:BWP0:RBC?')        # BWP RB Allocation
    cmod = s.query(f':CONF:NR5G:{ldir}:CC1:FRAM1:BWP0:SLOT0:ALL0:MOD?')  # channel Modulation
    tpre = s.query(f':CONF:NR5G:UL:CC1:TPR?')                       # Trans Precoding State
    phas = s.query(f':CONF:NR5G:UL:CC1:RFUC:STAT?')                 # Phase comp state
    time = s.query(':SENS:SWE:TIME?')                               # measure time
    nslt = s.query(':SENS:NR5G:FRAM:SLOT?')                         # number of slots
    s.close()

    outStr = f'{freq}GHz_{frng}_{ldir}_{chbw}_{bscs}_{bwrb}_{cmod}_TP{tpre}_PhaseComp{phas} {time}sec slots:{nslt}'
    print(outStr)
    return outStr

if __name__ == "__main__":
    get_5GNR_settings()
