""" Rohde & Schwarz Automation for demonstration use."""
import pyvisa as visa

def vQuery(SCPI):                           # Socket Query
    vWrite(SCPI)
    sOut = instr.query(SCPI)
    print(f'Query: {sOut}')
    return sOut

def vWrite(SCPI):                           # Socket Write
    print(f'Write: {SCPI}')
    instr.write(SCPI)

rm = visa.ResourceManager()
instr = rm.open_resource(f'TCPIP0::192.168.58.115::inst0::INSTR')
# s.settimeout(5)

vQuery(f'*IDN?')
vQuery(f'*OPT?')

# HISLP: TCPIP0::192.168.1.100::hislip0::INSTR
# VXI11: TCPIP0::192.168.1.100::inst0::INSTR
# TCPIP: TCPIP0::192.168.1.100::INSTR
# Sckt : TCPIP0::192.168.1.100::999::SOCKET
# USB  : USB::0x0AAD::<Modl>::<SerN>::INSTR
# RSUSB: RSNRP::<Modl>::<SerN>::INSTR
# GPIB : GPIB0::20::INSTR
# Seril: ASRL3::INSTR
