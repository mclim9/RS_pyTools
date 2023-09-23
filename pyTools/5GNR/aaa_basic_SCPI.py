
FSW = iSocket().open('192.168.58.109', 5025)
FSW.write('INIT:CONT OFF')                                  # Continuous Sweep off
FSW.write(f':SENSE:FREQ:CENT {freq}')                       # CW Center Freq
FSW.query(f':SENS:ADJ:LEV;*OPC?')                           # AutoLevel
FSW.query('INIT:IMM;*OPC?')                                 # Single Sweep
EVM = FSW.query(':FETC:CC1:SUMM:EVM:ALL:AVER?')             # FSW CW
attn = FSW.query('INP:ATT?')                                # Input Attn
refl = FSW.query('DISP:TRAC:Y:SCAL:RLEV?')                  # Reference Level
chPw = FSW.query(':FETC:CC1:ISRC:FRAM:SUMM:POW?')           # FSW CW Ch Pwr

SMW = iSocket().open('192.168.58.114', 5025)
SMW.write(f':SOUR1:FREQ:CW {freq}')                         # SMW center freq
SMW.write(f':SOUR1:POW:POW {pwr}')                          # SMW Power
