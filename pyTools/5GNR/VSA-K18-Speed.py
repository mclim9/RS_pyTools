from iSocket import iSocket                         # Import socket module

FSW = iSocket().open('192.168.58.109', 5025)
SMW = iSocket().open('192.168.58.114', 5025)
FSW.timeout(5)                                   # Timeout in seconds

def System_Init():
    FSW.write(':INST:CRE:NEW AMPL, "Amplifier"')        # Amplifier App
    FSW.write(':INIT:CONT OFF')                         # Single  Sweep
    FSW.write(':CONF:GEN:IPC:ADR "192.168.58.114"')     # SMW IP Address
    FSW.write(':SENS:PMET1:FREQ:LINK CENT')             # Power Meter Freq
    FSW.write(':CONF:GEN:CONN:STAT ON;*WAI')            # Connect SMW
    FSW.write(':CONF:REFS:CGW:AMOD:STAT ON')            # Arb Mode ON
    FSW.write(':CONF:REFS:CGW:READ;*WAI')               # Read Wavefom
    FSW.write(':TRIG:SEQ:SOUR EXT')                     # Trigger Output
    SMW.write(':SOUR1:BB:ARB:TRIG:OUTP1:MODE REST')     # Arb Marker Restart
    FSW.tick()
    FSW.query(':INIT:IMM;*OPC?')
    FSW.tock('K18 sweep')

def K18_Short_Capture():
    FSW.write(':CONF:EST:FULL OFF')
    FSW.write(':CONF:EST:STOP 0.001')
    FSW.write(':CONF:EVAL:FULL OFF')
    FSW.write(':CONF:EVAL:STOP 0.001')
    FSW.write(':SENS:SWE:TIME:AUTO OFF')
    FSW.write(':SENS:SWE:TIME 0.003')
    FSW.tick()
    FSW.query(':INIT:IMM;*OPC?')
    FSW.tock('Short Capture')

def K18_Calc_DPD():
    FSW.tick()
    FSW.write(':CONF:DDPD:STAT ON')
    FSW.write(':CONF:DDPD:COUN 5')
    FSW.opc(':CONF:DDPD:STAR')
    FSW.write(':CONF:DDPD:APPL:STAT ON')
    FSW.tock('DPD Calculation')

def K18_Apply_MM():
    FSW.write(':CONF:MDPD:STAT ON')                             # Memory Model ON
    FSW.write(':CALC:MDPD:MOD;*WAI')                            # Create MM
    FSW.tick()
    FSW.query(':CONF:MDPD:WAV:UPD;*OPC?')                       # Apply to waveform
    FSW.tock('Apply DPD')

def NR5G_Config():
    FSW.write(':INST:CRE:NEW NR5G, "5G NR"')                    # 5G
    FSW.write(':INIT:CONT OFF')                                 # Single  Sweep
    FSW.write(':SENS:FREQ:CENT 1e9')                            # Center Freq
    FSW.query(':SENS:ADJ:LEV;*OPC?')                            # Autolevel
    FSW.write(':CONF:NR5G:DL:CC1:DFR MIDD')                     # Freq Range
    FSW.write(':CONF:NR5G:DL:CC1:BW BW100')                     # RFBW
    FSW.write(':CONF:NR5G:DL:CC1:FRAM1:BWP0:RBC 273')           # BWP RB
    FSW.write(':CONF:NR5G:DL:CC1:FRAM1:BWP0:CSL 1')             # Slot def
    FSW.write(':CONF:NR5G:DL:CC1:FRAM1:BWP0:SLOT0:ALC 1')       # # of Ch
    FSW.write(':CONF:NR5G:DL:CC1:FRAM1:BWP0:SLOT0:CRSC 0')      # # of Corset
    FSW.write(':CONF:NR5G:DL:CC1:FRAM1:BWP0:SLOT0:ALL0:RBC 273')
    FSW.write(':CONF:NR5G:DL:CC1:FRAM1:BWP0:SLOT0:ALL0:SOFF 0')
    FSW.write(':CONF:NR5G:DL:CC1:FRAM1:BWP0:SLOT0:ALL0:SCO 14')
    FSW.write(':CONF:NR5G:DL:CC1:FRAM1:BWP0:SLOT0:ALL0:CW:MOD QPSK')
    FSW.write(':CONF:NR5G:DL:CC1:RFUC:FZER:MODE MAN')
    FSW.write(':CONF:NR5G:DL:CC1:RFUC:STAT OFF')                # Phase Comp Off
    FSW.write(':CONF:NR5G:DL:CC1:IDC ON')                       # Ignore DC
    FSW.write(':TRIG:SEQ:SOUR EXT')                             # Trigger Output

def NR5G_EVM():
    FSW.write(':CONF:NR5G:MEAS EVM')
    FSW.write(':SENS:SWE:TIME 0.001')
    FSW.write(':SENS:NR5G:FRAM:COUN:AUTO OFF')
    FSW.write(':SENS:NR5G:FRAM:SLOT 1')
    FSW.tick()
    FSW.query(':INIT:IMM;*OPC?')
    FSW.tock('K144 EVM time')

    FSW.write(':CONF:NR5G:MEAS ACLR')
    FSW.tick()
    FSW.query(':INIT:IMM;*OPC?')
    FSW.tock('K144 ACLR time')


if __name__ == '__main__':
    # System_Init()
    # K18_Short_Capture()
    # K18_Calc_DPD()
    K18_Apply_MM()
    # NR5G_Config()
    # NR5G_EVM()
