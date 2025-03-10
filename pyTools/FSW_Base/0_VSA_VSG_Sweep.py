from iSocket import iSocket                                         # Import socket module

def FSW_Setup():
    s.query(f':INST:SEL "Spectrum";*OPC?')
    s.query(f'*RST;*OPC?')
    s.write(f':SYST:DISP:UPD ON')
    s.write(f':INIT:CONT OFF')
    s.write(f':SENS:FREQ:CENT 1600000000')
    s.write(f':SENS:FREQ:SPAN 1900000000')
    s.write(f':DISP:WIND:TRAC:Y:SCAL:RLEV 10')
    s.write(f':INP:ATT:AUTO OFF')
    s.write(f':INP:ATT:AUTO ON')
    s.write(f':SENS:WIND1:DET1:FUNC POS')
    s.write(f':DISP:WIND1:SUBW:TRAC1:MODE MAXH')
    s.write(f':INIT:CONT ON')

def SMW_Sweep():
    smw = iSocket().open('172.24.225.114', 5025)
    base_freq = 1.6e9 - 190e6
    for i in range(38):
        delta = i * 10e6
        smw.write(f':SOUR1:FREQ:CW {base_freq + delta}')
        smw.delay(1)
    return 0

if __name__ == "__main__":
    s = iSocket().open('172.24.225.128', 5025)
    FSW_Setup()
    SMW_Sweep()
