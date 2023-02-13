""" Rohde & Schwarz RTP Amplitude Measurement"""
from NR5G import PVT                             # Import socket module
from iSocket import iSocket
from math import log10

VSG = 'PVT'
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
        pvt.query('CONF:GPRF:GEN:SPAT:USAG ON, OFF, OFF, OFF, OFF, OFF, OFF, OFF;*OPC?')    # VSG Routing
        pvt.write(f'SOUR:GPRF:GEN1:ARB:FILE "@WAVEFORM/{wave}.wv"')
        pvt.query('ROUT:NRS:MEAS:SPAT "RF1.1";*OPC?')                                       # VSA Routing
        pvt.write(f'TRIG:NRS:MEAS:MEV:SOUR "GPRF Gen1: Restart Marker"')                    # VSA Trig
        smw.query('OUTP1:STAT 0;*OPC?')
    elif VSG == 'SMW':
        pvt.query('SOUR:GPRF:GEN1:STAT OFF;*OPC?')                                          # VSG OFF
        smw.query('OUTP1:STAT 1;*OPC?')
        pvt.query('ROUT:NRS:MEAS:SPAT "RF1.8";*OPC?')                                       # VSA Routing
        pvt.write(f'TRIG:NRS:MEAS:MEV:SOUR "Base1: External TRIG A"')                       # VSA Trig

def set_freq(freq):
    pvt.write(f':CONF:NRS:MEAS1:CC1:FREQ {freq}')                       # PVT Meas 5G
    if VSG == 'PVT':
        pvt.query(f':SOUR:GPRF:GEN1:RFS:FREQ {freq};*OPC?')             # PVT Generator
    elif VSG == 'SMW':
        smw.query(f':SOUR1:FREQ:CW {freq};*OPC?')                       # SMW


def set_power(power):
    pvt.write(f':CONF:NRS:MEAS:RFS:ENP {power}')                        # PVT Meas 5G
    if VSG == 'PVT':
        pvt.query(f':SOUR:GPRF:GEN1:RFS:LEV {power};*OPC?')             # PVT Generator
    elif VSG == 'SMW':
        smw.query(f':SOUR1:POW:POW {power};*OPC?')                      # SMW

def meas_EVM():
    pvt.query(':INIT:NRS:MEAS:MEV;*OPC?')                               # Single Sweeep
    # rdStr = pvt.query(f'FETC:NRS:MEAS:MEV:CC1:EVM:MAX?')
    rdStr = pvt.query(f'FETC:NRS:MEAS:MEV:CC1:MOD:AVER?').split(',')    # EVM table
    outStr = f'{rdStr[3]}, {rdStr[17]}'                                 # 4:EVMRMS 18:Tx_Pwr
    # pvt.clear_error()
    return outStr

def main():
    global VSG
    file_write('Instrument,Freq,Wave,Pwr,EVM_%,tx_power,EVM_dB')
    for vsg in ['PVT']:
        VSG = vsg
        init_system()
        for freq in [6.6e9, 6.7e9, 6.8e9, 6.9e9, 7.0e9]:
            set_freq(freq)
            for pwr in range(-50, 5, 1):
                set_power(pwr)
                evm = meas_EVM()
                evm_per = float(evm.split(',')[0])
                evm_db = 20 * log10(evm_per / 100)
                outStr = f'{vsg}_2_{VSA}, {freq:.0f}, {wave}, {pwr}, {evm}, {evm_db:5.2f}'
                file_write(outStr)


if __name__ == "__main__":
    pvt = PVT().open('192.168.58.30', 5025)
    smw = iSocket().open('192.168.58.114', 5025)
    wave = 'FR1_UL_100MHz_30SCS_256QAM'
    main()
