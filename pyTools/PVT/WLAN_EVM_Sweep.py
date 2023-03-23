""" Rohde & Schwarz RTP Amplitude Measurement"""
from NR5G import PVT                             # Import socket module
from iSocket import iSocket

VSG = 'SMW'
VSA = 'PVT'                 # FSW | PVT

def file_write(outString):
    filename = __file__.split('.')[0] + '.csv'
    fily = open(filename, '+a')
    fily.write(f'{outString}\n')
    print(outString)
    fily.close()

def init_system():
    if VSG == 'PVT':
        pvt.query('SOUR:GPRF:GEN1:STAT ON;*OPC?')
        pvt.write('ROUT:GPRF:GEN:SPAT "RF1.1-RF1.8"')
        pvt.query('CONF:GPRF:GEN:SPAT:USAG ON, OFF, OFF, OFF, OFF, OFF, OFF, OFF;*OPC?')
        pvt.query('ROUT:NRS:MEAS:SPAT "RF1.1";*OPC?')
        pvt.write(f'SOUR:GPRF:GEN1:ARB:FILE "@WAVEFORM/{wave}.wv"')
        pvt.write(f'TRIG:WLAN:MEAS:MEV:SOUR "IF Power"')
        smw.query('OUTP1:STAT 0;*OPC?')
    elif VSG == 'SMW':
        pvt.query('SOUR:GPRF:GEN1:STAT OFF;*OPC?')
        smw.query('OUTP1:STAT 1;*OPC?')
        pvt.query('ROUT:NRS:MEAS:SPAT "RF1.8";*OPC?')
        pvt.write(f'TRIG:WLAN:MEAS:MEV:SOUR "Base1: External TRIG A"')

def set_freq(freq):
    pvt.write(f'CONF:WLAN:MEAS1:RFS:FREQ {freq}')                       # PVT Meas WLAN
    if VSG == 'PVT':
        pvt.query(f':SOUR:GPRF:GEN1:RFS:FREQ {freq};*OPC?')             # PVT Generator
    elif VSG == 'SMW':
        smw.query(f':SOUR1:FREQ:CW {freq};*OPC?')                       # SMW


def set_power(power):
    pvt.write(f'CONF:WLAN:MEAS:RFS:ENP1 {power}')                       # PVT Meas RMS Pwr
    if VSG == 'PVT':
        pvt.query(f':SOUR:GPRF:GEN1:RFS:LEV {power};*OPC?')             # PVT Generator
    elif VSG == 'SMW':
        smw.query(f':SOUR1:POW:POW {power};*OPC?')                      # SMW

def get_crest():
    if VSG == 'PVT':
        rms = pvt.queryFloat('SOUR:GPRF:GEN1:RFS:LEV?')                 # PVT RMS power
        peak = pvt.queryFloat('SOUR:GPRF:GEN1:RFS:PEP?')                # PVT Peak Power
    elif VSG == 'SMW':
        rms = smw.queryFloat(':SOUR1:POW:POW?')                         # SMW RMS power
        peak = smw.queryFloat(':SOUR1:POW:PEP?')                        # SMW Peak Power
    crest = peak - rms
    pvt.write(f'CONF:WLAN:MEAS1:RFS:UMAR1 {crest}')
    return crest

def meas_EVM():
    pvt.query(':INIT:WLAN:MEAS:MEV;*OPC?')                              # Single Sweeep
    pvt.query(':CONF:WLAN:MEAS1:MEV:SCO:MOD 20;*OPC?')                  # Num Averages
    rdStr = pvt.query(f'FETC:WLAN:MEAS:MEV:TRAC:EVM:SYMB:AVER?').split(',')   # EVM table
    outStr = f'{rdStr[1]},{rdStr[1]}'                                   # 5:EVMRMS 18:Tx_Pwr
    # pvt.clear_error()
    return outStr

def main():
    global VSG
    crest = get_crest()
    file_write('Instrument,Freq,Wave,CF,Pwr,EVM_%,tx_power,EVM_dB,')
    for vsg in ['PVT', 'SMW']:
        VSG = vsg
        init_system()
        for freq in [5.18e9, 5.925e9, 7.125e9]:
            set_freq(freq)
            for pwr in range(-50, 0, 1):
                set_power(pwr)
                evm = meas_EVM()
                evm_db = float(evm.split(',')[0])
                evm_per = pow(10, evm_db / 20) * 100
                outStr = f'{vsg}_2_{VSA}, {freq:.0f}, {wave}, {crest}, {pwr}, {evm_per:5.3f}, n/a, {evm_db:5.2f}'
                file_write(outStr)


if __name__ == "__main__":
    pvt = PVT().open('192.168.58.30', 5025)
    smw = iSocket().open('192.168.58.114', 5025)
    wave = 'WLAN_320MHz_MCS13'
    main()
