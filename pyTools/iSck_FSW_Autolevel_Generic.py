"""Rohde & Schwarz Automation for IQ Analyzer use."""
from iSocket import iSocket                                         # Import socket module

# ##############################################################################
# ## Main Code
# ##############################################################################
def get_Settings():
    freq = s.queryFloat(':SENS:FREQ:CENT?') / 1e9       # Center Frequency
    refl = s.queryFloat('DISP:TRAC:Y:SCAL:RLEV?')       # Reference Level
    attn = s.queryInt(':INP:ATT?')                      # Input Attn
    pamp = s.queryInt(':INP:GAIN:STAT?')                # Preamp
    ovld = s.queryInt('STAT:QUES:POW:COND?')            # Overload Status
    print(f'{freq}GHz_{refl:6.2f}dBm_{attn:2d}dB_PA{pamp}_Ovld{ovld}')
    return [freq, refl, attn, pamp]

def Get_Ovld_Stat():
    s.query('INIT:IMM;*OPC?')
    Read = int(s.query('STAT:QUES:POW:COND?'))
    # RF_Ovld = Read & 1
    # RF_Udld = Read & 2
    # IF_Ovld = Read & 4
    return Read

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
    # s.write(':CONF:POW:AUTO ONCE;*WAI')               # 802.11
    s.write(':SENS:ADJ:LEV;*WAI')                       # Spec; 5GNR; IQ_Analyzer
    get_Settings()

    while Get_Ovld_Stat() == 0:
        shift_attn(-1)
        if (get_Settings()[2] == 0):                    # Get Attn
            end_attn_delta = 0
            break
    shift_attn(1)

    num_loop = 0
    while (Get_Ovld_Stat() == 0) and (num_loop < 10):
        shift_RefLvl(-1)
        if get_Settings()[1] > 30:                      # Ref Level
            break
        num_loop += 1
    shift_RefLvl(1)

    if Get_Ovld_Stat() > 1:                             # Final IF Overload check

        shift_RefLvl(1)
    get_Settings()

if __name__ == "__main__":
    s = iSocket().open('192.168.58.109', 5025)
    optimize_FrontEnd()
