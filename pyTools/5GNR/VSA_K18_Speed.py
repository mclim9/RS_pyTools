from iSocket import iSocket                             # Import socket module

def System_Init(FSW, SMW):
    # SMW.write(':SOUR1:BB:ARB:WAV:SEL "/var/user/NR5G"')
    SMW.write(':SOUR1:BB:ARB:TRIG:OUTP1:MODE REST')     # Arb Marker Restart

    FSW.write(':INST:CRE:NEW AMPL, "Amplifier"')        # Amplifier App
    FSW.write(':INST:SEL "Amplifier"')
    FSW.write(':INIT:CONT OFF')                         # Single  Sweep
    FSW.write(':CONF:GEN:IPC:ADR "192.168.58.114"')     # SMW IP Address
    FSW.write(':SENS:PMET1:FREQ:LINK CENT')             # Power Meter Freq
    FSW.query(':CONF:GEN:CONN:STAT ON;*OPC?')           # Connect SMW
    FSW.write(':CONF:REFS:CGW:AMOD:STAT ON')            # Arb Mode ON
    FSW.query(':CONF:REFS:CGW:READ;*OPC?')              # Read Wavefom
    FSW.write(':SENS:SWE:TIME:AUTO ON')                 # Sweeptime on
    FSW.write(':TRIG:SEQ:SOUR EXT')                     # Trigger Output
    capTime = FSW.queryFloat(':SENS:SWE:TIME?')         # Sweep Time

    FSW.tick()
    FSW.query(':INIT:IMM;*OPC?')
    FSW.tock(f'K18 EVM {capTime*1000} msec Calc')

def K18_Get_EVM(FSW):
    rdStr = FSW.query(':FETC:MACC:REVM:CURR:RES?')
    print(rdStr)
    return rdStr

def K18_Short_Capture(FSW):
    FSW.write(':CONF:EST:FULL OFF')                     # Estimate Full OFF
    FSW.write(':CONF:EST:STOP 0.0005')                  # Estimate 1mSec
    FSW.write(':CONF:EVAL:FULL OFF')                    # Sync: Full OFF
    FSW.write(':CONF:EVAL:STOP 0.0005')                 # Sync: 1mSec
    FSW.write(':SENS:SWE:TIME:AUTO OFF')                # Sweeptime off
    FSW.write(':SENS:SWE:TIME 0.0006')                  # Sweeptime 1.1msec
    FSW.write(':TRIG:SEQ:HOLD:TIME -2e-6')              # Trigger offset
    capTime = FSW.queryFloat(':SENS:SWE:TIME?')         # Sweep Time
    FSW.tick()
    FSW.opc(':INIT:IMM')
    FSW.tock(f'K18 EVM {capTime*1000} msec Calc')

def K18_PowerServo(FSW, SMW, DesiredPwr):
    FSW.write(':INIT:CONT OFF')                         # Single  Sweep
    FSW.tick()
    for i in range(2):
        FSW.query(':INIT:IMM;*OPC?')
        SMWPwr = SMW.queryFloat(':SOUR1:POW:POW?')
        FSWPwr = FSW.queryFloat(':FETC:POW:OUTP:CURR:RES?')         # K18 Pwr
        PwrDel = DesiredPwr - FSWPwr
        SMW.write(f':SOUR1:POW:POW {SMWPwr + PwrDel}')
        # RMSPwr = FSW.query(':FETC:POW:SENS:IN:CURR:RES?')         # NRP Pwr
    FSW.tock('FSW Power Servo')
    return FSWPwr

def K18_Calc_DPD(FSW):
    FSW.tick()
    FSW.write(':CONF:DDPD:STAT ON')
    FSW.write(':CONF:DDPD:COUN 5')
    FSW.opc(':CONF:DDPD:STAR')
    FSW.write(':CONF:DDPD:APPL:STAT ON')
    FSW.tock('DPD Calculation')

def K18_Apply_MM(FSW):
    FSW.write(':CONF:MDPD:STAT ON')                             # Memory Model ON
    FSW.write(':CALC:MDPD:MOD;*WAI')                            # Create MM
    # FSW.write(':CONF:MDPD:APPL:MOD "C:\\R_S\\instr\\user\\K18\\ReferenceFiles\\NR5G.wv"')
    FSW.write(':CONF:MDPD:APPL:MOD "C:\\R_S\\instr\\user\\K18\\ReferenceFiles\\5G_FR1_30KHzSCS_100MHz-500uSec.wv"')
    FSW.tick()
    FSW.query(':CONF:MDPD:WAV:UPD;*OPC?')                       # Apply to waveform
    FSW.tock('Apply DPD')

def NR5G_Config(FSW):
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

def NR5G_EVM(FSW):
    FSW.write(':CONF:NR5G:MEAS EVM')
    FSW.write(':SENS:SWE:TIME 0.0006')
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
    FSW = iSocket().open('192.168.58.109', 5025)
    SMW = iSocket().open('192.168.58.114', 5025)
    FSW.timeout(5)                                          # Timeout in seconds

    # System_Init(FSW, SMW)
    # K18_Short_Capture(FSW)
    K18_PowerServo(FSW, SMW, -30)
    # K18_Calc_DPD(FSW)
    K18_Apply_MM(FSW)
    # NR5G_Config(FSW)
    # NR5G_EVM(FSW)
    # K18_Get_EVM(FSW)
