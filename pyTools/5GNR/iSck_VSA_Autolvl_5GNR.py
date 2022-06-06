""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module
oldEVM = 0

def get_Settings():
    freq = s.queryFloat(':SENS:FREQ:CENT?') / 1e9       # Center Frequency
    refl = s.queryFloat('DISP:TRAC:Y:SCAL:RLEV?')       # Reference Level
    attn = s.queryInt(':INP:ATT?')                      # Input Attn
    # pamp = s.queryInt(':INP:GAIN:STAT?')                # Preamp
    pamp = 9999
    s.query('INIT:IMM;*OPC?')
    ovld = s.queryFloat(':FETC:CC1:ISRC:FRAM:SUMM:EVM:ALL:AVER?')            # Overload Status
    print(f'{freq}GHz,{refl:6.2f}dBm,{attn:2d}dB,PA{pamp},EVM:{ovld:.2f}')
    return [freq, refl, attn, pamp]

def Get_EVM_Stat():
    global oldEVM
    s.query('INIT:IMM;*OPC?')
    # newEVM = float(s.query(':FETC:EVM:ALL:AVER?'))      # WLANAD
    newEVM = float(s.query(':FETC:CC1:ISRC:FRAM:SUMM:EVM:ALL:AVER?'))      # WLANAD
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
    s.write('INIT:CONT OFF')
    s.write(f':INP:ATT:AUTO OFF')
    s.write(f':DISP:TRAC:Y:SCAL:RLEV 0')

    # s.write(':CONF:POW:AUTO ONCE;*WAI')               # 802.11 AL
    # s.write(':SENS:ADJ:LEV;*WAI')                     # Spec; 5GNR; IQ_Analyzer AL
    get_Settings()

    num_loop = 0
    while (Get_EVM_Stat() > 0) and (num_loop < 20):
        shift_RefLvl(-1)
        if get_Settings()[1] > 30:                      # Ref Level
            break
        num_loop += 1
    shift_RefLvl(1)

    end_attn_delta = -1
    while Get_EVM_Stat() > 0:
        shift_attn(1)
        if (get_Settings()[2] == 0):                    # Get Attn
            end_attn_delta = 0
            break
    shift_attn(end_attn_delta)
    get_Settings()

if __name__ == "__main__":
    s = iSocket().open('192.168.58.109', 5025)
    optimize_FrontEnd()
