""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket
import timeit
oldEVM = 0

def get_Settings():
    freq = s.queryFloat(':SENS:FREQ:CENT?') / 1e9       # Center Frequency
    refl = s.queryFloat('DISP:TRAC:Y:SCAL:RLEV?')       # Reference Level
    attn = s.queryInt(':INP:ATT?')                      # Input Attn
    # pamp = s.queryInt(':INP:GAIN:STAT?')              # Preamp
    pamp = 9999                                         # no Preamp in FE
    tick = timeit.default_timer()
    timeDelta = timeit.default_timer() - tick
    print(f'{freq}GHz, {refl:6.2f}dBm,{attn:2d}dB, PA{pamp}, oldEVM:{oldEVM:.2f}, {timeDelta * 1000:.3f}msec')

    return [freq, refl, attn, pamp]

def Get_EVM_Stat():
    global oldEVM
    s.query('INIT:IMM;*OPC?')
    newEVM = float(s.query(':FETC:CC1:ISRC:FRAM:SUMM:EVM:ALL:AVER?'))      # 5GNR
    delta = oldEVM - newEVM
    oldEVM = newEVM
    return delta

def shift_RefLvl(delta):
    refl = s.query('DISP:TRAC:Y:SCAL:RLEV?')            # Reference Level
    refl = float(refl)
    s.write(f':DISP:TRAC:Y:SCAL:RLEV {refl + delta}')

def shift_attn(delta):
    attn = s.query(':INP:ATT?')                         # Attenuation
    attn = float(attn)
    s.write(f':INP:ATT {attn + delta}')

def optimize_FrontEnd():
    tick = timeit.default_timer()
    s.write('INIT:CONT OFF')
    s.write(f':INP:ATT:AUTO OFF')
    s.write(f':INP:ATT 0')
    # s.write(':SENS:ADJ:LEV;*WAI')                             # 5GNR Autolevel
    chPwr = s.queryFloat(f':FETC:CC1:ISRC:FRAM:SUMM:POW:AVER?') # Get 5G Power(dBm)
    s.write(f':DISP:TRAC:Y:SCAL:RLEV {chPwr + 12}')
    get_Settings()

    end_attn_delta = -1
    while Get_EVM_Stat() > 0:
        shift_attn(2)
        if (get_Settings()[2] == 0):                    # Get Attn
            end_attn_delta = 0
            break
    shift_attn(end_attn_delta)
    get_Settings()

    num_loop = 0
    while (Get_EVM_Stat() > 0) and (num_loop < 10):
        shift_RefLvl(-2)
        if get_Settings()[1] > 30:                      # Ref Level
            break
        num_loop += 1
    shift_RefLvl(1)
    timeDelta = timeit.default_timer() - tick
    print(f'TTime: {timeDelta:.6f} sec')

if __name__ == "__main__":
    s = iSocket().open('192.168.10.40', 5025)
    optimize_FrontEnd()
