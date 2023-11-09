""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module
from iSck_FSW_5GNR_GetSettings import get_5GNR_settings

# #############################################################################
# ## Main Code
# #############################################################################
freq      = 24e9
pwr     = -20
numPts    = 100
slot_arry = [1, 2, 3, 5, 10, 20, 30, 50, 79]
slot_time = 126e-6
filename  = __file__.split('.py')[0] + '.txt'

fileOut = open(filename, 'a')
FSW = iSocket().open('192.168.58.109', 5025)
FSW.s.settimeout(15)
fileOut.write(f'{FSW.idn}\n')
SMW = iSocket().open('192.168.58.114', 5025)
fileOut.write(f'{SMW.idn}\n')
fileOut.write(f'{get_5GNR_settings()}\n')
fileOut.write('Num,Freq,Power [dBm],RefLvl [dBm],Attn[dB],ChPwr[dBm],EVM [dB],swpTime[ms],slots\n')

FSW.write('INIT:CONT OFF')
# FSW.write(f':SENS:FREQ:CENT {freq}')                # Center Freq
# FSW.write(f'DISP:TRAC:Y:SCAL:RLEV {pwr}')
for slot_Cnt in slot_arry:
    swpTime = slot_time * slot_Cnt
    FSW.write(':SENS:NR5G:FRAM:COUN:AUTO OFF')
    FSW.write(f':SENS:NR5G:FRAM:COUN 1')
    FSW.write(f':SENS:NR5G:FRAM:SLOT {slot_Cnt}')
    FSW.write(f':SENS:SWE:TIME {swpTime}')
    FSW.write('INIT:CONT OFF')
    for i in range(numPts):
        FSW.query('INIT:IMM;*OPC?')
        # EVM = FSW.query(':FETC:CC1:SUMM:EVM:ALL:AVER?')       # FSW
        EVM = FSW.queryFloat(':FETC:CC1:ISRC:FRAM:SUMM:EVM:ALL?')    # FSVA
        attn = FSW.query('INP:ATT?')                            # Input Attn
        refl = FSW.query('DISP:TRAC:Y:SCAL:RLEV?')
        chPw = FSW.queryFloat(':FETC:CC1:ISRC:FRAM:SUMM:POW?')  # Channel Pwr

        data = f'{i},{freq},{pwr},{refl},{attn},{chPw:7.3f},{EVM:7.3f},{swpTime * 1000:.6f},{slot_Cnt}'
        print(data)
        fileOut = open(filename, 'a')
        fileOut.write(f'{data}\n')
        fileOut.close()
