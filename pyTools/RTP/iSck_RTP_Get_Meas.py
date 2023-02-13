""" Rohde & Schwarz RTP Amplitude Measurement"""
from iSocket import iSocket                         # Import socket module

def RTP_Get_Meas(mg):
    # data = rtp.query(f':MEAS{mg}:ARES?')          # Entire Table
    # print(len(data.split(',')))                   # Verify number of elements
    amp = rtp.query(f'MEAS{mg}:RES:AVG? AMPL')      # Amplitude
    dlt = rtp.query(f'MEAS{mg}:RES:AVG? DEL')       # Delay
    phs = 'n/a'
    # phs = rtp.query(f'MEAS{mg}:RES:AVG? PHAS')    # Phase
    return f'{amp}, {dlt}, {phs}'

def RTP_Offset(ch, skew, attn_dB):
    rtp.write(f'CHAN{ch}:SKEW:TIME {skew}')         # -100e9 to 100e9 / 10e-15
    rtp.write(f'CHAN{ch}:EATS LOG')                 # LIN LOG
    rtp.write(f'CHAN{ch}:EATT {attn_dB}')           # -60 to 120 dB

def RTP_sweepCount(num):
    rtp.write(f':MEAS:STAT:RES')                    # Reset Meas Stats
    for i in range(num):
        self.init_imm()

def file_write(outString):
    filename = __file__.split('.')[0] + '.csv'
    fily = open(filename, '+a')
    fily.write(f'{outString}\n')
    fily.close()

def RTP_Offset(ch, skew, attn_dB):
    rtp.write(f'CHAN{ch}:SKEW:TIME {skew}')         # -100e9 to 100e9 / 10e-15
    rtp.write(f'CHAN{ch}:EATS LIN')                 # LIN LOG
    rtp.write(f'CHAN{ch}:EATT {attn_dB}')           # -60 to 120 dB

def main():
    rtp = iSocket().open('192.168.10.50', 5025)
    rtp.s.settimeout(5)
    IDN = rtp.query('*IDN?')

    meas1 = float(RTP_Get_Meas(1).split(',')[0])
    meas2 = float(RTP_Get_Meas(2).split(',')[0])
    meas3 = float(RTP_Get_Meas(3).split(',')[0])
    meas4 = float(RTP_Get_Meas(4).split(',')[0])
    # file_write(f'{meas1},{meas2},{meas3},{meas4}')

    print(f'Ratio2 {meas1/meas2}')
    print(f'Ratio3 {meas1/meas3}')
    print(f'Ratio4 {meas1/meas4}')

    RTP_Offset(2, 100e9, 1.234)

    rtp.clear_error()

if __name__ == "__main__":
    main()
