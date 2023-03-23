from iSocket import iSocket

def RTP_ChSetup():
    rtp.query(f'DIFF1:STAT OFF; *OPC?')
    for ch in range(4):
        rtp.write(f'CHAN{ch + 1}:STAT ON')          # State ON
        rtp.write(f'CHAN{ch + 1}:INV OFF')          # Inverse OFF
        rtp.write(f'CHAN{ch + 1}:SCAL 0.03')        # Vertical Scale, V
        # rtp.write(f'CHAN{ch + 1}:OFFS -0.1')        # Offset
        rtp.write(f'CHAN{ch + 1}:SKEW:TIME 0')      # -100e9 to 100e9 / 10e-15
        rtp.write(f'CHAN{ch + 1}:EATS LOG')         # LIN LOG
        rtp.write(f'CHAN{ch + 1}:EATT 0')           # -60 to 120 dB
    rtp.write(f'CHAN2:INV ON')

def RTP_MeasSetup(i, CH1):
    rtp.write(f':MEAS{i}:ENAB ON')                  # Turn on measurement
    rtp.write(f':MEAS{i}:SOUR C{CH1}W1')
    rtp.write(f':MEAS{i}:STAT:ENAB 1')              # Statistics on
    rtp.write(f':MEAS{i}:CAT AMPT')                 # Amp & Time Measurments
    rtp.write(f':MEAS{i}:MAIN AMPL')                # Main Amplitude
    rtp.write(f':MEAS{i}:ADD DTOT,ON')              # Delay to trigger
    rtp.write(f':MEAS:STAT:RES')                    # Reset Meas Stats

def RTP_B7_Pulse_Source():
    rtp.write(f'PSRC:STAT ON')                      # Pulse Source ON
    rtp.write(f'PSRC:OUTP -{pulse_Volt}')           # Output Level
    rtp.write(f'PSRC:REPR 10e6')                    # Output Frequency

def RTP_Trigger_Config():
    rtp.write(f'TRIG:LEV1:VAL -{pulse_Volt / 2}')

def RTP_Deskew():
    RTP_B7_Pulse_Source()
    RTP_ChSetup()
    RTP_Trigger_Config()
    rtp.write(f'TIM:SCAL 20e-12')
    rtp.write(f'CHAN1:OFFS -{pulse_Volt / 2}')      # Offset
    rtp.write(f'CHAN2:OFFS {pulse_Volt / 2}')       # Offset
    rtp.write(f'CHAN3:STAT OFF')
    rtp.write(f'CHAN4:STAT OFF')
    RTP_MeasSetup(1, 1)
    RTP_MeasSetup(2, 2)

def RTP_Verify():
    rtp.write(f':MEAS1:ENAB OFF')                   # Turn on measurement
    rtp.write(f':MEAS2:ENAB OFF')                   # Turn on measurement
    rtp.write(f':MEAS3:ENAB OFF')                   # Turn on measurement
    rtp.write(f':MEAS4:ENAB OFF')                   # Turn on measurement
    rtp.query(f'DIFF1:STAT ON; *OPC?')
    rtp.write(f'TIM:SCAL 200e-12')
    rtp.write(f'CHAN2:INV OFF')
    rtp.write(f'CHAN1:OFFS -{pulse_Volt / 2}')      # Offset
    rtp.write(f'CHAN2:OFFS -{pulse_Volt / 2}')      # Offset
    rtp.write(f'DIFF1:COUP OFF')
    rtp.write('DIFF1:COMM:SCAL 0.003')
    rtp.write('DIFF1:DIFF:SCAL 0.040')

if __name__ == "__main__":
    rtp = iSocket().open('192.168.10.50', 5025)
    rtp.s.settimeout(5)
    IDN = rtp.query('*IDN?')
    pulse_Volt = 0.2

    RTP_Deskew()
    Skew1 = rtp.query(f'MEAS1:RES:AVG? DTOT')      # Amplitude
    Skew2 = rtp.query(f'MEAS2:RES:AVG? DTOT')      # Amplitude
    print(f'{Skew1} {Skew2}')
    RTP_Verify()
