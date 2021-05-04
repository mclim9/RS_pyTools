""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module
from iSck_FSW_5GNR_GetSettings import get_5GNR_settings

def get_SMW_FE_Lock():
    asdf = SMW.query(':SCON:EXT:RF1:RCON:STAT?')
    print(asdf)

def set_FExx_freq(freq):
    # ## Config FSVA-->FE
    FSW.query(f':SENS:EFR1:CONN:STAT ON;*OPC?')         # Connect FE
    FSW.query(f':SENS:EFR1:CONN:STAT ON;*OPC?')         # Connect FE
    # FSW.delay(1)
    FSW.write(f':SENS:FREQ:CENT {freq}')                # Center Freq

    # ## Config SMW-->FE
    FSW.query(f':SENS:EFR1:CONN:STAT OFF;*OPC?')        # Disconnect FE
    FSW.query(f':SENS:EFR1:CONN:STAT OFF;*OPC?')        # Disconnect FE
    # FSW.delay(1)
    SMW.write(f':SOUR:FREQ:CW {freq}')                  # Center Freq
    # SMW.query(':SOUR1:CORR:FRES:RF:OPT:LOC;*OPC?')    #

def set_FExx_amp(pwr):
    # ## Config FSVA-->FE
    FSW.query(f':SENS:EFR1:CONN:STAT ON;*OPC?')         # Connect FE
    FSW.query(f':SENS:EFR1:CONN:STAT ON;*OPC?')         # Connect FE
    FSW.write('INIT:CONT OFF')                          # Single Sweep
    FSW.query('INIT:IMM;*OPC?')
    # chPwr = FSW.queryFloat(':FETC:CC1:ISRC:FRAM:SUMM:POW?')           # Ch Pwr
    chPwr = pwr - 12
    FSW.write(f':INP:ATT 0')
    FSW.write(f'DISP:TRAC:Y:SCAL:RLEV {chPwr}')

    # ## Config SMW-->FE
    FSW.query(f':SENS:EFR1:CONN:STAT OFF;*OPC?')        # Disconnect FE
    FSW.query(f':SENS:EFR1:CONN:STAT OFF;*OPC?')        # Disconnect FE
    # FSW.delay(1)
    SMW.write(f'SOUR:POW:LEV:IMM:AMPL {pwr}')           # RF Pwr

# #############################################################################
# ## Main Code
# #############################################################################
freq_arry = range(int(49e9), int(50.1e9), int(100e6))
pwr_arry = range(-45, 5, 1)
# freq_arry = range(int(46e9), int(47e9), int(50e6))
# pwr_arry = [-10, -8, -6, -4, -2]
filename = __file__.split('.py')[0] + '.txt'

fileOut = open(filename, 'a')
FSW = iSocket().open('192.168.58.105', 5025)
FSW.s.settimeout(15)
fileOut.write(f'{FSW.idn}\n')
SMW = iSocket().open('192.168.58.114', 5025)
# SMW.write(':SOUR1:EFR:CMOD RXTX')
SMW.write(':SOUR1:EFR:TRXM:STAT ON')
fileOut.write(f'{SMW.idn}\n')
fileOut.write(f'{get_5GNR_settings()}\n')
fileOut.write('Mode,Freq,Power [dBm],RefLvl [dBm],Attn[dB],ChPwr[dBm],EVM [dB],AutoLvl\n')

set_FExx_freq(49e9)
set_FExx_amp(-40)
set_FExx_freq(36e9)
set_FExx_amp(-50)

FSW.write('INIT:CONT OFF')
FSW.write(':SENS:NR5G:FRAM:COUN:AUTO OFF')
FSW.write(':SENS:NR5G:FRAM:COUN 1')
for mode in ['LEV']:
    for freq in freq_arry:
        set_FExx_freq(freq)
        for pwr in pwr_arry:
            set_FExx_amp(pwr)
            FSW.write('INIT:CONT OFF')
            FSW.query('INIT:IMM;*OPC?')
            # EVM = FSW.query(':FETC:CC1:SUMM:EVM:ALL:AVER?')       # FSW
            EVM = FSW.query(':FETC:CC1:ISRC:FRAM:SUMM:EVM:ALL?')    # FSVA
            FSW.query(f':SENS:EFR1:CONN:STAT ON;*OPC?')             # Connect FE
            FSW.query(f':SENS:EFR1:CONN:STAT ON;*OPC?')             # Connect FE
            attn = FSW.query('INP:ATT?')                            # Input Attn
            refl = FSW.query('DISP:TRAC:Y:SCAL:RLEV?')
            chPw = FSW.queryFloat(':FETC:CC1:ISRC:FRAM:SUMM:POW?')  # Channel Pwr

            data = f'{mode},{freq},{pwr},{refl},{attn},{chPw},{EVM},RMS-12'
            print(data)
            fileOut = open(filename, 'a')
            fileOut.write(f'{data}\n')
            fileOut.close()
