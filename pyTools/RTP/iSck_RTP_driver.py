""" Rohde & Schwarz RTP Amplitude Measurement"""
from iSocket import iSocket                             # Import socket module

class DSO(iSocket):
    def __init__(self):
        super().__init__()

    def ChSetup(self):
        for ch in range(4):
            self.write(f'CHAN{ch + 1}:STAT ON')          # State ON
            self.write(f'CHAN{ch + 1}:INV OFF')          # Inverse OFF
            self.write(f'CHAN{ch + 1}:SCAL 0.02')        # Vertical Scale, V
            self.write(f'CHAN{ch + 1}:SKEW:TIME 0')      # -100e9 to 100e9 / 10e-15
            self.write(f'CHAN{ch + 1}:EATS LOG')         # LIN LOG
            self.write(f'CHAN{ch + 1}:EATT 0')           # -60 to 120 dB
        self.write(f'CHAN2:INV ON')
        self.write(f'CHAN4:INV ON')

    def meas_config(self, i, CH1, CH2):
        self.write(f':MEAS{i}:SOUR C{CH1}W1,C{CH2}W1')
        self.write(f':MEAS{i}:STAT:ENAB 1')              # Statistics on
        self.write(f':MEAS{i}:CAT AMPT')                 # Amp & Time Measurments
        self.write(f':MEAS{i}:MAIN AMPL')                # Main Amplitude
        # self.write(f':MEAS{i}:ADD RMS,ON')             # Add RMS
        self.write(f':MEAS{i}:ADD DEL,ON')               # Add Delay
        self.write(f':MEAS{i}:ADD PHAS,ON')              # Add Phase
        self.write(f':MEAS:STAT:RES')                    # Reset Meas Stats

    def Get_Meas(self, mg):
        # data = self.query(f':MEAS{mg}:ARES?')          # Entire Table
        # print(len(data.split(',')))                   # Verify number of elements
        amp = self.query(f'MEAS{mg}:RES:AVG? AMPL')      # Amplitude
        dlt = self.query(f'MEAS{mg}:RES:AVG? DEL')       # Delay
        phs = 'n/a'
        # phs = self.query(f'MEAS{mg}:RES:AVG? PHAS')    # Phase
        return f'{amp}, {dlt}, {phs}'

    def offset(self, ch, skew, attn_dB):
        self.write(f'CHAN{ch}:SKEW:TIME {skew}')         # -100e9 to 100e9 / 10e-15
        self.write(f'CHAN{ch}:EATS LOG')                 # LIN LOG
        self.write(f'CHAN{ch}:EATT {attn_dB}')           # -60 to 120 dB

    def init_imm(self):
        self.query('RUNS;*OPC?')                         # INIT:IMM

    def SweepContinuous(self, state):
        if state in ('ON', 'on', '1'):
            self.write('RUN')                            # Continuous sweep
        elif state in ('OFF', 'off', '0'):
            self.write('SING')                           # Single Sweep
        else:
            print(f'Invalid State: {state}')

    def sweepCount(self, num):
        self.write(f':MEAS:STAT:RES')                    # Reset Meas Stats
        for i in range(num):
            self.init_imm()

    def file_write(outString):
        filename = __file__.split('.')[0] + '.csv'
        fily = open(filename, '+a')
        fily.write(f'{outString}\n')
        fily.close()

if __name__ == "__main__":
    rtp = DSO().open('192.168.10.40', 5025)
    rtp.s.settimeout(5)
    print(rtp.query('*IDN?'))
