""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

def print_params():
    RFA_Pwr = SMW.queryFloat('SOUR1:POW:LEV?')
    RFA_PEP = SMW.queryFloat('SOUR1:POW:PEP?')
    RFA_LO = SMW.queryFloat(f':OUTPut1:AFIXed:RANGe:LOWer?')
    RFA_UP = SMW.queryFloat(f':OUTPut1:AFIXed:RANGe:UPPer?')

    RFB_Pwr = SMW.queryFloat('SOUR2:POW:LEV?')
    RFB_PEP = SMW.queryFloat('SOUR2:POW:PEP?')
    RFB_LO = SMW.queryFloat(f':OUTPut2:AFIXed:RANGe:LOWer?')
    RFB_UP = SMW.queryFloat(f':OUTPut2:AFIXed:RANGe:UPPer?')
    print(f'RFA:{RFA_Pwr:6.2f} {RFA_PEP:6.2f} {RFA_LO:6.2f} {RFA_UP:6.2f} RFB:{RFB_Pwr:6.2f} {RFB_PEP:6.2f} {RFB_LO:6.2f} {RFB_UP:6.2f}')

# #############################################################################
# ## Main Code
# #############################################################################
SMW = iSocket().open('192.168.58.103', 5025)

SMW.query(f'OUTP1 0;*OPC?')
SMW.query(f'OUTP2 0;*OPC?')
SMW.write(f':SOUR1:FREQ:CW 3775e6')
SMW.write(f':SOUR2:FREQ:CW 3775e6')
SMW.query(':SOUR1:FREQ:LOSC:MODE COUP;*OPC?')   # Couple LO
SMW.write(':SCON:OUTP:MAPP:RF1:STR1:STAT 1')    # StreamA --> RFA
SMW.write(':SCON:OUTP:MAPP:RF2:STR1:STAT 1')    # StreamA --> RFB
SMW.write(':SOUR1:BB:ARB:WAV:SEL "/var/user/NR5G_FR2_UL_100MHz_120SCS.wv"')
SMW.query(':SOUR1:BB:ARB:STAT ON;*OPC?')
SMW.query(f':SOUR1:POW:LEV -40;*OPC?')
SMW.write(':SOUR1:IQ:DOH:STAT 1')


print_params()
for pwr in [-30, -20]:
    SMW.query(f':SOUR1:POW:LEV {pwr};*OPC?')
    print(f'Set SOURCE1 {pwr}')
    print_params()

    SMW.query(f':SOUR2:POW:LEV {pwr};*OPC?')
    print(f'Set SOURCE2 {pwr}')
    print_params()
