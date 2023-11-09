""" Rohde & Schwarz Automation for demonstration use."""
# Before use:   Configure FSW/SMW
#               EVM should be displayed on EVM screen
#               FSW EVM is triggered measurement
#               Below code intended for FExxx

from iSocket import iSocket
import timeit
oldEVM = 0

def get_Settings():
    s.write('UNIT:EVM DB')
    tick = timeit.default_timer()
    freq = s.queryFloat(':SENS:FREQ:CENT?') / 1e9       # Center Frequency (50mSec)
    tick = timeit.default_timer()
    freq = s.queryFloat(':SENS:FREQ:CENT?') / 1e9       # Center Frequency (130mSec)
    refl = s.queryFloat('DISP:TRAC:Y:SCAL:RLEV?')       # Reference Level
    attn = s.queryInt(':INP:ATT?')                      # Input Attn
    # pamp = s.queryInt(':INP:GAIN:STAT?')              # Preamp
    pamp = 9999                                         # no Preamp in FE
    timeDelta = timeit.default_timer() - tick
    print(f'{freq}GHz, {refl:6.2f}dBm,{attn:2d}dB, PA{pamp}, oldEVM:{oldEVM:.2f}, {timeDelta * 1000:.3f}msec')

    return [freq, refl, attn, pamp]

def Get_EVM_Stat():
    global oldEVM
    s.query('INIT:IMM;*OPC?')
    newEVM = float(s.query(':FETC:CC1:ISRC:FRAM:SUMM:EVM:ALL:AVER?'))      # 5GNR 1CC EVM
    delta = oldEVM - newEVM
    oldEVM = newEVM
    return delta

def shift_RefLvl(delta):
    s.query('INIT:IMM;*OPC?')                                   # Update screen
    refl = s.query('DISP:TRAC:Y:SCAL:RLEV?')                    # Set Ref Level
    refl = float(refl)
    s.write(f':DISP:TRAC:Y:SCAL:RLEV {refl + delta}')

def shift_attn(delta):
    attn = s.query(':INP:ATT?')                                 # Attenuation
    attn = float(attn)
    s.write(f':INP:ATT {attn + delta}')

def optimize_FrontEnd():
    tick = timeit.default_timer()
    s.write('INIT:CONT OFF')                                    # Stop screen updates
    s.write(f':INP:ATT:AUTO OFF')                               # Attn Manual
    s.write(f':INP:ATT 0')                                      # Attn = 0
    # s.write(':SENS:ADJ:LEV;*WAI')                             # 5GNR Autolevel
    s.query('INIT:IMM;*OPC?')                                   # Update screen
    chPwr = s.queryFloat(f':FETC:CC1:ISRC:FRAM:SUMM:POW:AVER?') # Get 5G Power(dBm)
    s.write(f':DISP:TRAC:Y:SCAL:RLEV {chPwr + 0}')              # Set Reflvl

    end_attn_delta = -1
    while Get_EVM_Stat() > 0:
        shift_attn(3)
        if (get_Settings()[2] == 0):                            # Break if Attn=0
            end_attn_delta = 0
            break
    shift_attn(end_attn_delta)

    num_loop = 0
    while (Get_EVM_Stat() > -.2) and (num_loop < 15):
        shift_RefLvl(-2)
        if get_Settings()[1] > 30:                              # Break RefLevel>30
            break
        num_loop += 1
    shift_RefLvl(2)
    timeDelta = timeit.default_timer() - tick
    get_Settings()
    print(f'TTime: {timeDelta:.6f} sec')

if __name__ == "__main__":
    s = iSocket().open('192.168.58.109', 5025)
    optimize_FrontEnd()
