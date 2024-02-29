from iSocket import iSocket                             # Import socket module

FSW = iSocket().open('192.168.58.109', 5025)
SMW = iSocket().open('192.168.58.114', 5025)
SMW.timeout(5)                                          # Timeout in seconds

def VSG_NR5G_Quickset():
    SMW.tick()
    SMW.write(':SOUR1:BB:NR5G:LINK DOWN')               # Link Direction
    SMW.write(':SOUR1:BB:NR5G:QCKS:GEN:DUPL TDD')       # QS TDD | FDD
    SMW.write(':SOUR1:BB:NR5G:QCKS:GEN:CARD FR1GT3')    # QS Freq Range
    SMW.write(':SOUR1:BB:NR5G:QCKS:GEN:CBW BW100')      # QS RFBW
    SMW.write(':SOUR1:BB:NR5G:QCKS:GEN:SCSP SCS30')     # QS SCS
    SMW.write(':SOUR1:BB:NR5G:QCKS:GEN:ES:RBN 273')     # QS RB
    SMW.write(':SOUR1:BB:NR5G:QCKS:GEN:ES:MOD QAM64')    # QS Mod: QPSK; QAM64; QAM256
    SMW.query(':SOUR1:BB:NR5G:QCKS:APPL;*OPC?')         # QS Apply
    SMW.query(':SOUR1:BB:NR5G:NODE:RFPH:MODE 0')        # Phase Comp Off
    SMW.write(':SOUR1:BB:NR5G:TRIG:OUTP1:MODE REST')    # Arb Marker Restart
    SMW.query(':SOUR1:BB:NR5G:STAT 1;*OPC?')            # 5GNR On
    SMW.tock('Quick Set to Memory')

def VSA_Ch_Select(chType, chName):
    chList = FSW.query('INST:LIST?')
    if (chName in chList) and (chType in chList):
        FSW.write(f':INST:SEL "{chName}"')              # Sel Ch 5G
    else:
        FSW.write(f':INST:CRE:NEW {chType}, "{chName}"')# Create ch

def VSA_NR5G_Config():
    VSA_Ch_Select('NR5G', '5G NR')                      # Select 5GNR
    FSW.write(':INIT:CONT OFF')                         # Single  Sweep
    FSW.query(':SENS:ADJ:LEV;*OPC?')                    # Autolevel
    FSW.write(':CONF:GEN:IPC:ADDR "192.168.58.114"')    # VSG IP Addr
    FSW.opc(':CONF:GEN:CONN:STAT ON')                   # Connect VSG
    FSW.write(':CONF:GEN:CONT:STAT ON')                 # VSG Control
    FSW.write(':CONF:GEN:RFO:STAT ON')                  # VSG RF
    FSW.write(':CONF:SETT:NR5G')                        # VSG 5G Setting Transfer
    # FSW.write(':CONF:NR5G:DL:CC1:RFUC:FZER:MODE MAN') # Phase Comp Freq
    FSW.write(':CONF:NR5G:DL:CC1:RFUC:STAT OFF')        # Phase Comp Off
    FSW.write(':CONF:NR5G:DL:CC1:IDC ON')               # Ignore DC
    FSW.write(':TRIG:SEQ:SOUR EXT')                     # Trigger Output

def VSA_NR5G_Meas():
    FSW.tick()                                          # Start Timer
    VSA_Ch_Select('NR5G', '5G NR')                      # Select 5GNR
    FSW.write(':CONF:NR5G:MEAS EVM')                    # Sel K144 EVM Meas
    FSW.write(':SENS:SWE:TIME 0.0006')                  # Capture Time
    FSW.write(':SENS:NR5G:FRAM:COUN:AUTO OFF')          # Frame auto off
    FSW.write(':SENS:NR5G:FRAM:SLOT 1')                 # Single slot
    FSW.tock('K144 Setup')                              # Stop Timer

    FSW.tick()                                          # Start Timer
    FSW.query(':INIT:IMM;*OPC?')                        # Take sweep
    a = FSW.queryFloat(':FETC:SUMM:EVM:PCH:AVER?')      # EVM Phy Ch Avg
    print(f'Meas :              EVM: {a:8.4f}')
    FSW.tock('K144 EVM time')                           # Stop Timer


if __name__ == '__main__':
    VSG_NR5G_Quickset()
    VSA_NR5G_Config()
    VSA_NR5G_Meas()
    FSW.write(':INIT:CONT ON')                          # Single  Sweep
