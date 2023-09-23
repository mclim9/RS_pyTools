""" Rohde & Schwarz Automation for demonstration use."""
import socket                               # Import socket module

def sQuery(SCPI):
    try:
        s.sendall(f'{SCPI}\n'.encode())         # Write SCPI
        sOut = s.recv(100000).decode().strip()  # Read socket
    except socket.error as errr:
        sOut = f'{SCPI} not Read {errr}'
    print(sOut)
    return sOut

SMW_IP = '192.168.58.114'
PVT_IP = '192.168.58.30'

s = socket.socket()
s.connect((SMW_IP, 5025))
s.settimeout(5)
sQuery(f'*IDN?')

Band = sQuery(':SOUR1:BB:NR5G:NODE:CELL0:CARD?')
Dir  = sQuery(':SOUR1:BB:NR5G:LINK?')
BW   = sQuery(':SOUR1:BB:NR5G:NODE:CELL0:CBW?')
if Dir == 'UP':
    allc = 0
    dir  = 'UL'
    ch  = 'PUSC'
elif Dir == 'DOWN':
    allc = 1
    dir  = 'DL'
    ch  = 'PDSC'

SCS  = sQuery(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:DL:BWP0:SCSP?')
Mod  = sQuery(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL{allc}:MOD?')
RBN  = sQuery(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL{allc}:RBN?')

SMW_FreqBnd = sQuery(f':SOUR1:BB:NR5G:NODE:CELL0:CARD?')
SMW_ChanBnd = sQuery(f':SOUR1:BB:NR5G:NODE:CELL0:CBW?')
SMW_BWPSCS  = sQuery(f':SOUR1:BB:NR5G:UBWP:USER0:CELL0:{dir}:BWP0:SCSP?')
SMW_BWPRB   = sQuery(f':SOUR1:BB:NR5G:UBWP:USER0:CELL0:{dir}:BWP0:RBN?')
SMW_BWPRBO  = sQuery(f':SOUR1:BB:NR5G:UBWP:USER0:CELL0:{dir}:BWP0:RBOF?')
SMW_ChanRB  = sQuery(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL{allc}:RBN?')
SMW_ChanRBO = sQuery(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL{allc}:RBOF?')
SMW_ChSymb  = sQuery(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL{allc}:SYMN?')
SMW_ChSymbO = sQuery(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL{allc}:SYM?')

SMW_configT = sQuery(f':SOUR1:BB:NR5G:UBWP:USER0:CELL0:{dir}:BWP0:{ch}:DMTA:CTYP?')
SMW_MapType = sQuery(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:MAPT?')
SMW_1stAPos = sQuery(f':SOUR1:BB:NR5G:NODE:CELL0:TAP?')
SMW_addPosi = sQuery(f':SOUR1:BB:NR5G:UBWP:USER0:CELL0:{dir}:BWP0:{ch}:DMTA:APIN?')
SMW_dmrsLen = sQuery(f':SOUR1:BB:NR5G:UBWP:USER0:CELL0:{dir}:BWP0:{ch}:DMTA:MLEN?')
SMW_relPowr = sQuery(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:{ch}:DMRS:POW?')
SMW_MMLayer = sQuery(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:{ch}:TXSC:NLAY?')
SMW_cdmGrup = sQuery(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:{ch}:TXSC:CDMD?')

Wavename = f'{Band}_{dir}_{SCS}SCS_{BW}_{RBN}RB_{Mod}'
print(f'{Wavename}')
s = socket.socket()
s.connect((PVT_IP, 5025))
s.settimeout(5)
sQuery(f'*IDN?')

sQuery(f'CONF:NRS:MEAS:CC1:CBAN {SMW_ChanBnd.replace("BW", "B")};*OPC?')
sQuery(f'CONF:NRS:MEAS:CC1:PLC {0};*OPC?')
sQuery(f'CONF:NRS:MEAS:CC1:TAP {SMW_1stAPos};*OPC?')

if "N" in SMW_BWPSCS:
    CP = 'NORM'
else:
    CP = 'EXT'
SCS = int(SMW_BWPSCS.replace('N','0'))
sQuery(f'CONF:NRS:MEAS:CC1:BWP BWP0,S{SCS}K,{CP},{SMW_BWPRB},{SMW_BWPRBO};*OPC?')
sQuery('SYST:ERR?')
sQuery('SYST:ERR?')
