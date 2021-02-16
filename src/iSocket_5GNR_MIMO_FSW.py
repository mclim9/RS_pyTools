"""Rohde & Schwarz Automation for demonstration use. """
from iSocket import iSocket                                             #Import socket module

# ##############################################################################
# ## Main Code
# ##############################################################################
s = iSocket().sOpen('192.168.58.109', 5025)
# s.settimeout(1)                                                       # Timeout in seconds

AntPort = 1000
s.sWrite(':SENS:FREQ:CENT 1e9')                                         # Center Frequency
s.sWrite(':INST:CRE:NEW NR5G, "5G NR"')                                 # Start 5GNR
s.sWrite(':INIT:CONT ON')                                               # Continuous Sweep
s.sWrite(':MMEM:LOAD:DEM:CC1 "C:\\R_S\\Instr\\user\\Demo\\5GNR-FR2-Demo\\DL-100MHz-120kHz-256QAM.allocation"')
if AntPort == 1000:
    s.sWrite(':CONF:NR5G:DL:CC1:PAM1:STAT ON')                          # PDSCH AntPort 1000
else:
    s.sWrite(':CONF:NR5G:DL:CC1:PAM2:STAT ON')                          # PDSCH AntPort 1001
s.sWrite(':CONF:NR5G:DL:CC1:IDC ON')                                    # Ignore DC
s.sWrite(':CONF:NR5G:DL:CC1:RFUC:STAT OFF')                             # Phase Compensation OFF
s.sWrite(':CONF:NR5G:DL:CC1:FRAM1:BWP0:SLOT0:ALL0:CLM LC21')            # PDSCH Layers 2/1
s.sWrite(':CONF:NR5G:DL:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:AP 1000, 1001')  # PDSCH Antenna ports 0,1