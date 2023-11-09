""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module
from iSck_FSW_5GNR_GetSettings import get_5GNR_settings

freq_arry = [int(42.7e9), int(43.1007e9)]
freq_arry = [int(3.6e9)]
pwr_arry = range(-50, 5, 1)
pwr_arry = [-10]

def file_write(outString):
    filename = __file__.split('.py')[0] + '.txt'
    fily = open(filename, '+a')
    fily.write(f'{outString}\n')
    print(outString)
    fily.close()

FSW = iSocket().open('192.168.58.109', 5025)
FSW.s.settimeout(60)
file_write(FSW.idn)
SMW = iSocket().open('192.168.58.114', 5025)
file_write(SMW.idn)
file_write(get_5GNR_settings())
file_write('Mode,Freq,Power [dBm],RefLvl [dBm],Attn[dB],ChPwr[dBm],EVM[dB],Leveling,IQNC,Time[Sec]')

FSW.write('INIT:CONT OFF')                                          # Single Sweep
FSW.write(':SENS:NR5G:FRAM:COUN:AUTO OFF')                          # Frame count off
FSW.write(':SENS:NR5G:FRAM:COUN 1')                                 # Single frame
# FSW.write(':SENS:NR5G:RSUM:CCR ALL')                              # CA View all CC results
for mode in ['LEV']:                                                # LEV:autolevel EVM:autoEVM
    for freq in freq_arry:
        # FSW.write(f':CONF:NR5G:GMCF {freq}')                      # CA Center Freq
        FSW.write(f':SENSE:FREQ:CENT {freq}')                       # CW Center Freq
        SMW.write(f':SOUR1:FREQ:CW {freq}')                         # SMW center freq
        for pwr in pwr_arry:
            for iqnc in [1, 2, 5, 10, 20, 30, 50]:
                SMW.write(f':SOUR1:POW:POW {pwr}')                      # SMW Power
                FSW.query(f':SENS:ADJ:{mode};*OPC?')                    # AutoEVM or Level
                FSW.write(f':SENS:ADJ:NCAN:AVER:COUN {iqnc}')           # Set IQ NC Averages
                FSW.write('INIT:CONT OFF')
                FSW.tick()
                FSW.query('INIT:IMM;*OPC?')
                time = FSW.tock()
                EVM = FSW.queryFloat(':FETC:CC1:SUMM:EVM:ALL:AVER?')    # FSW CW
                # EVM = FSW.queryFloat(':FETC:ALL:SUMM:EVM:PCH?')       # FSW CC
                # EVM = FSW.query(':FETC:CC1:ISRC:FRAM:SUMM:EVM:ALL?')  # FSVA
                attn = FSW.query('INP:ATT?')                            # Input Attn
                refl = FSW.query('DISP:TRAC:Y:SCAL:RLEV?')
                chPw = FSW.queryFloat(':FETC:CC1:ISRC:FRAM:SUMM:POW?')  # FSW CW Ch Pwr
                # chPw = FSW.queryFloat(':FETC:ALL:SUMM:POW?')          # FSW CA Ch Pwr

                data = f'{mode},{freq},{pwr},{refl},{attn},{chPw:6.2f},{EVM:6.2f},{mode},{iqnc},{time}'
                file_write(data)
