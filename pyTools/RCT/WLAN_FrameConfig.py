""" Rohde & Schwarz RTP Amplitude Measurement"""
from Base import PVT
from iSocket import iSocket

def PVT_config_WLAN_frame():
    BW = 80
    pvt.write(f':CONF:WLAN:MEAS1:MEV:REP SING')                             # Sweep mode: SING | CONT
    pvt.write(f':CONF:WLAN:MEAS1:ISIG:RMOD SISO')                           # MIMO: SISO | TMIM
    pvt.write(f':CONF:WLAN:MEAS1:ISIG:STAN VHT')                            # Standard: n:HTOF ac:VHT ax:HEOF be:EHT
    pvt.write(f':CONF:WLAN:MEAS1:ISIG:BWID BW{BW}')                         # Bandwidth: 20 40 80 16 32
    pvt.clear_error()

def SMW_config_WLAN_frame():
    BW = 80
    smw = iSocket().open('192.168.58.114', 5025)
    smw.write(f':SOUR1:BB:WLNN:BW BW{BW}')                                  # Bandwidth
    smw.write(f':SOUR1:BB:WLNN:FBL:TMOD HT')                                # n:HT ac:V ax:HE be:EHT
    smw.write(f':SOUR1:BB:WLNN:FBL:MOD QAM256')                             # QAM64 QAM256 QAM1024 QAM4094
    smw.clear_error()

def SMW_config_WLAN():
    smw = iSocket().open('192.168.58.114', 5025)
    smw.write(':SOUR1:CORR:OPT:EVM 1')                                      # EVM Opt
    smw.write(':SOUR1:BB:WLNN:TRIG:OUTP1:MODE REST')                        # Arb Restart
    smw.write(':SOUR1:INP:USER6:DIR OUTP')                                  # USER6 Output
    smw.write(':OUTP1:USER6:SIGN MARKA1')                                   # USER6 Marker1

if __name__ == "__main__":
    pvt = PVT().open('192.168.58.30', 5025)
    pvt.s.settimeout(5)
    # SMW_config_WLAN()
    # SMW_config_WLAN_frame()
    PVT_config_WLAN_frame()
    pvt.clear_error()
