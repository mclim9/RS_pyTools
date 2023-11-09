""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

def file_write(outString):
    filename = __file__.split('.py')[0] + '.txt'
    fily = open(filename, '+a')
    fily.write(f'{outString}\n')
    print(outString)
    fily.close()

FSW = iSocket().open('192.168.58.109', 5025)
FSW.s.settimeout(30)
file_write(FSW.idn)
file_write('Freq[MHz],RefLvl[dBm],Attn[dB],ChPwr[dBm],EVM[dB],ALev,Capture Time,Slots,AL Time, EVM Time')

FSW.write('INIT:CONT OFF')                                          # Single Sweep
FSW.write(':SENS:NR5G:FRAM:COUN:AUTO OFF')                          # Frame count off
FSW.write(':SENS:NR5G:FRAM:COUN 1')                                 # Single frame
FSW.write(':CONF:NR5G:DL:C1:IDC ON')                                # Ignore DC
for mode in ['LEV']:                                                # LEV:autolevel EVM:autoEVM
    freq = FSW.queryFloat(f':SENSE:FREQ:CENT?')                     # CW Center Freq
    for slot in [1, 1, 2, 5, 10, 20, 40, 'ALL']:
        FSW.write(f':SENS:NR5G:FRAM:SLOT {slot}')                   # Number of slots
        FSW.tick()
        FSW.query(f':SENS:ADJ:{mode};*OPC?')                        # AutoEVM or Level
        AL_time = FSW.tock()
        FSW.write('INIT:CONT OFF')
        FSW.tick()
        FSW.query('INIT:IMM;*OPC?')
        EVM = FSW.queryFloat(':FETC:CC1:SUMM:EVM:ALL:AVER?')        # FSW CW
        EVM_time = FSW.tock()
        FSW.write(':INP:ATT:AUTO OFF')                              # Manual Attn
        attn = FSW.queryFloat('INP:ATT?')                           # Attn Setting
        refl = FSW.queryFloat('DISP:TRAC:Y:SCAL:RLEV?')
        time = FSW.queryFloat('SENS:SWE:TIME?')                     # Sweep Time
        slot = FSW.query(':SENS:NR5G:FRAM:SLOT?')                   # Number of slots
        chPw = FSW.queryFloat(':FETC:CC1:ISRC:FRAM:SUMM:POW?')      # FSW CW Ch Pwr

        data = f'{freq/1e6},{refl:6.2f},{attn:3.0f},{chPw:6.2f},{EVM:6.2f},{mode},{time:6.2f},{slot:4s},{AL_time:6.3f},{EVM_time:6.3f}'
        file_write(data)
