""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module


FSW = iSocket().open('192.168.58.109', 5025)
FSW.s.settimeout(30)

FSW.write(':TRIG:SEQ:SOUR EXT')                                         # External Trigger

FSW.write(':CONF:NR5G:LDIR UL')                                         # UL | DL
FSW.write(':CONF:NR5G:UL:CC1:DFR HIGH')                                 # HIGH
FSW.write(':CONF:NR5G:UL:CC1:TPR ON')                                   # Trans Precoding
FSW.write(':CONF:NR5G:UL:CC1:FRAM1:BWP0:SSP SS120')                     # SS15 | SS30 | SS60 | SS120
FSW.write(':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:ALL0:MOD QAM64')          # QAM16 | QAM64

FSW.write(':SENS:SWE:TIME 0.000500')                                    # Capture time
FSW.write(':SENS:NR5G:FRAM:SLOT 1')                                     # Measure 1 slots
FSW.write(':SENS:NR5G:FRAM:COUN:STAT OFF')                              # Frame Count: OFF

FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:CTYP 1')       # Config Type: 1 | 
FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:MTYP A')       # Mappng Type: A | B
FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:TAP 2')        # 1st DMRS Sy: 2 | 3
FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:MSYM:APOS 2')  # Add Pos Inx: 0 | 1 | 2 | 3
FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:MSYM:LENG 1')  # DMRS Length: 1 | 2
FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:CGWD 2')       # CDM Group
FSW.query('INIT:IMM;*OPC?')

for i in range(10):
    errMsg = FSW.query('SYST:ERR?')
    if errMsg.split(',')[0] == '0':
        break
    print(errMsg)
