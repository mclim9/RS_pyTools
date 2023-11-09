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
    print(f'{RFA_Pwr:6.2f} {RFA_PEP:6.2f} {RFA_LO:6.2f} {RFA_UP:6.2f} {RFB_Pwr:6.2f} {RFB_PEP:6.2f} {RFB_LO:6.2f} {RFB_UP:6.2f}')

# #############################################################################
# ## Main Code
# #############################################################################
SMW = iSocket().open('192.168.58.103', 5025)

SMW.query(f'OUTP1 1;*OPC?')
SMW.query(f'OUTP2 1;*OPC?')
SMW.query(f':SOUR1:POW:LEV -100;*OPC?')
SMW.query(f':SOUR2:POW:LEV -100;*OPC?')

for pwr in [-10, -20]:
    SMW.query(f':SOUR1:POW:LEV {pwr};*OPC?')
    print(f'Set SOURCE1 {pwr}')
    print_params()

    SMW.query(f':SOUR2:POW:LEV {pwr};*OPC?')
    print(f'Set SOURCE2 {pwr}')
    print_params()
