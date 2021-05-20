"""Rohde & Schwarz Automation for demonstration use. """
from iSocket import iSocket                                         # Import socket module

# ##############################################################################
# ## Main Code
# ##############################################################################
def get_5GNR_AL_Setting():
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

def get_5GNR_autolevel():
    s.write('INIT:CONT OFF')
    get_5GNR_AL_Setting()

    # """ Optimising for attenuation """
    end_attn_delta = 1
    while Get_Ovld_Stat() == 0:
        shift_attn(-1)
        data = get_5GNR_AL_Setting()
        if (data[2] == 0):
            end_attn_delta = 0
            break
    shift_attn(end_attn_delta)

    # """ Optimising for reference level """
    while Get_Ovld_Stat() == 0:
        shift_RefLvl(-1)
        refL = get_5GNR_AL_Setting()[1]
        if refL > 30:
            break

    # """ Final check for IF Overload """
    if Get_Ovld_Stat() > 1:
        shift_RefLvl(1)
    get_5GNR_AL_Setting()

if __name__ == "__main__":
    s = iSocket().open('192.168.58.109', 5025)
    get_5GNR_autolevel()
