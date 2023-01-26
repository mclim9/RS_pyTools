""" Rohde & Schwarz RTP Amplitude Measurement"""
from iSocket import iSocket                         # Import socket module

def RTP_ChSetup():
    for ch in range(4):
        instr.write(f'CHAN{ch + 1}:STAT ON')        # State ON
        instr.write(f'CHAN{ch + 1}:INV OFF')        # Inverse OFF
        instr.write(f'CHAN{ch + 1}:SCAL 0.02')      # Vertical Scale, V
        instr.write(f'CHAN{ch + 1}:SKEW:TIME 0')    # -100e9 to 100e9 / 10e-15
        instr.write(f'CHAN{ch + 1}:EATS LOG')       # LIN LOG
        instr.write(f'CHAN{ch + 1}:EATT 0')         # -60 to 120 dB
    instr.write(f'CHAN2:INV ON')
    instr.write(f'CHAN4:INV ON')

def RTP_meas_config(i, CH1, CH2):
    instr.write(f':MEAS{i}:SOUR C{CH1}W1,C{CH2}W1')
    instr.write(f':MEAS{i}:STAT:ENAB 1')            # Statistics on
    instr.write(f':MEAS{i}:CAT AMPT')               # Amp & Time Measurments
    instr.write(f':MEAS{i}:MAIN AMPL')              # Main Amplitude
    # instr.write(f':MEAS{i}:ADD RMS,ON')           # Add RMS
    instr.write(f':MEAS{i}:ADD DEL,ON')             # Add Delay
    instr.write(f':MEAS{i}:ADD PHAS,ON')            # Add Phase
    instr.write(f':MEAS:STAT:RES')                  # Reset Meas Stats

def RTP_Get_Meas(mg):
    # data = instr.query(f':MEAS{mg}:ARES?')        # Entire Table
    # print(len(data.split(',')))                   # Verify number of elements
    amp = instr.query(f'MEAS{mg}:RES:AVG? AMPL')    # Amplitude
    dlt = instr.query(f'MEAS{mg}:RES:AVG? DEL')     # Delay
    phs = 'n/a'
    # phs = instr.query(f'MEAS{mg}:RES:AVG? PHAS')  # Phase
    return f'{amp}, {dlt}, {phs}'

def RTP_Offset(ch, skew, attn_dB):
    instr.write(f'CHAN{ch}:SKEW:TIME {skew}')       # -100e9 to 100e9 / 10e-15
    instr.write(f'CHAN{ch}:EATS LOG')               # LIN LOG
    instr.write(f'CHAN{ch}:EATT {attn_dB}')         # -60 to 120 dB

def RTP_init_imm():
    instr.query('RUNS;*OPC?')                       # INIT:IMM

def RTP_SweepContinuous(state):
    if state in ('ON', 'on', '1'):
        instr.write('RUN')                          # Continuous sweep
    elif state in ('OFF', 'off', '0'):
        instr.write('SING')                         # Single Sweep
    else:
        print(f'Invalid State: {state}')

def RTP_sweepCount(num):
    instr.write(f':MEAS:STAT:RES')                  # Reset Meas Stats
    for i in range(num):
        RTP_init_imm()

def file_write(outString):
    filename = __file__.split('.')[0] + '.csv'
    fily = open(filename, '+a')
    fily.write(f'{outString}\n')
    fily.close()

if __name__ == "__main__":
    smw = iSocket().open('192.168.10.30', 5025)
    instr = iSocket().open('192.168.10.50', 5025)
    instr.s.settimeout(5)
    IDN = instr.query('*IDN?')

    RTP_ChSetup()
    for i in range(1, 5, 1):
        RTP_meas_config(i, i, 1)

    for freq in range(int(100e6), int(5e9), int(100e6)):
        smw.write(f'SOUR2:FREQ:CW {freq}')
        smw.write(f'OUTP2:STAT 1')
        # instr.write(f'ACQ:RES {8/freq}')          # Resolution
        instr.write(f'TIM:RANG {1.2/freq}')         # Acquisition Time

        RTP_sweepCount(100)
        meas1 = RTP_Get_Meas(1)
        meas2 = RTP_Get_Meas(2)
        meas3 = RTP_Get_Meas(3)
        meas4 = RTP_Get_Meas(4)
        file_write(f'{freq},{meas1},{meas2},{meas3},{meas4}')

    instr.clear_error()
