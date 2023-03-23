""" Rohde & Schwarz RTP Amplitude Measurement"""
from NR5G import PVT                             # Import socket module
from iSocket import iSocket

def PVT_config_5G_frame():
    RB = 273                                                                # BW20:51 BW100:273
    pvt.write(f':CONF:NRS:MEAS:MEV:PCOM OFF, 0')                            # Phase Compensation
    pvt.write(f':CONF:NRS:MEAS1:CC1:CBAN B100')                             # Bandwidth
    pvt.write(f':CONF:NRS:MEAS1:CC1:TAP 2')                                 # Type A Position
    pvt.write(f':CONF:NRS:MEAS1:CCAL1:TXBW:SCSP S30K')                      # TX BW
    pvt.write(f':CONF:NRS:MEAS:CC1:BWP BWP0, S30K, NORM, {RB}, 0')          # User --> BWP
    pvt.write(f':CONF:NRS:MEAS1:CC1:BWP:PUSC:DMTA BWP0, 1, 0, 1')           # Config; AddPos; MaxLength
    pvt.write(f':CONF:NRS:MEAS1:CC1:BWP:PUSC:DMTB BWP0, 1, 0, 1')           # Config; AddPos; MaxLength
    pvt.write(f'CONF:NRS:MEAS:CC1:ALL1:PUSC A, 14, 0, OFF, {RB}, 0, Q256')  # <MappingType>, <NoSymbols>, <StartSymbol>, <Auto>, <NoRBs>, <StartRB>, <ModScheme>
    pvt.write(f'CONF:NRS:MEAS1:CC1:ALL1:PUSC:ADD 1, 0, 1')                  # <DMRSLength>, <AntennaPort>, <CDMGroups>

def SMW_config_5G_frame():
    RB = 273
    smw = iSocket().open('192.168.58.114', 5025)
    smw.write(':SOUR1:BB:NR5G:LINK UP')
    smw.write(':SOUR1:BB:NR5G:NODE:CELL0:CBW BW100')                        # Bandwidth
    smw.write(':SOUR1:BB:NR5G:NODE:CELL0:CARD FR1GT3')                      # Freqeuncy
    smw.write(':SOUR1:BB:NR5G:NODE:RFPH:MODE 0')                            # Phase Compensation
    smw.write(f':SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:SCSP N30')          # Sub Carrier Spacing
    smw.write(f':SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:RBN {RB}')          # BWP RB
    smw.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:RBN {RB}')   # Ch RB
    smw.write(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:MOD QAM256')  # Modulation
    smw.clear_error()

def SMW_config_5G():
    smw = iSocket().open('192.168.58.114', 5025)
    smw.write(':SOUR1:CORR:OPT:EVM 1')                                      # EVM Opt
    smw.write(':SOUR1:BB:NR5G:TRIG:OUTP1:MODE REST')                        # Arb Restart
    smw.write(':SOUR1:INP:USER6:DIR OUTP')                                  # USER6 Output
    smw.write(':OUTP1:USER6:SIGN MARKA1')                                   # USER6 Marker1

if __name__ == "__main__":
    pvt = PVT().open('192.168.58.30', 5025)
    pvt.s.settimeout(5)
    # SMW_config_5G()
    # SMW_config_5G_frame()
    PVT_config_5G_frame()
    pvt.clear_error()
