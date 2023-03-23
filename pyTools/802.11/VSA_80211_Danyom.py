""" Rohde & Schwarz Automation for demonstration use."""
import socket

def sWrite(SCPI):                           # Socket Write
    print(f'Write: {SCPI}')
    s.sendall(f'{SCPI}\n'.encode())

def main():
    sWrite(':INIT:CONT OFF')                                   # Single sweep
    sWrite(':SENS:FREQ:CENT 6000000000')
    sWrite(':CONF:STAN 10')                                    # 802.11ax
    sWrite(':SENS:SWE:TIME 0.01')                              # Capture time
    sWrite(':TRAC:IQ:SRAT 3.2e+8')                             # Sampling Rate
    sWrite(':TRIG:SEQ:SOUR EXT')                               # Ext Trigger
    sWrite(':CONF:WLAN:RUC:HEPP MU')                           # HE MU-PPDU(DL)
    sWrite(':SENS:DEM:FORM:BAN:BTYP:AUTO:TYPE AIHS')           # Demod --> PPDU Format to Measure
    sWrite(':CONF:WLAN:RUC:SEGM1:CHAN1:RUL1:USER:MCS 11')      # MCS
    sWrite(':CONF:WLAN:RUC:COUN:ACT 1')                        
    sWrite(':CONF:WLAN:GTIM:AUTO:TYPE L2G1')                   # Guard Interval Time 7.2uSec
    sWrite(':INIT:IMM;*WAI')

if __name__ == "__main__":
    s = socket.socket()
    s.connect(('192.168.58.109', 5025))
    main()
