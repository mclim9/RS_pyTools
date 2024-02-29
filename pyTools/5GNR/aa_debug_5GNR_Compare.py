""" Rohde & Schwarz Automation for demonstration use."""
import socket

def sQuery(SCPI):
    try:
        s.sendall(f'{SCPI}\n'.encode())         # Write SCPI
        sOut = s.recv(100000).decode().strip()  # Read socket
    except socket.error as errr:
        sOut = f'{SCPI} not Read {errr}'
    return sOut

FSW_IP = '192.168.58.109'
SMW_IP = '192.168.58.114'

dir = 'UL'  # UL | DL
if dir == 'DL':
    allc = 1
    ch  = 'PDSC'
else:
    allc = 0
    ch  = 'PUSC'

s = socket.socket()
s.connect((FSW_IP, 5025))
sQuery('INIT:IMM;*OPC?')
FSW_FreqBnd = sQuery(f':CONF:NR5G:{dir}:CC1:DFR?')
FSW_ChanBnd = sQuery(f':CONF:NR5G:{dir}:CC1:BW?')
FSW_RefPntA = sQuery(f':CONF:NR5G:{dir}:CC1:RPA:RTCF?')
FSW_BWPSCS  = sQuery(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SSP?')
FSW_BWPRB   = sQuery(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:RBC?')
FSW_BWPRBO  = sQuery(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:RBOF?')
FSW_ChanRB  = sQuery(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:RBC?')
FSW_ChanRBO = sQuery(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:RBOF?')
FSW_ChSymb  = sQuery(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:SCO?')
FSW_ChSymbO = sQuery(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:SOFF?')
# --------------
FSW_configT = sQuery(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:CTYP?')
FSW_MapType = sQuery(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:MTYP?')
FSW_1stAPos = sQuery(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:TAP?')
FSW_addPosi = sQuery(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:MSYM:APOS?')
FSW_dmrsLen = sQuery(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:MSYM:LENG?')
FSW_relPowr = sQuery(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:POW?')
FSW_MMLayer = sQuery(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:CLM?')
FSW_cdmGrup = sQuery(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:CGWD?')
# SSB Stuff
if dir == 'DL':
    FSW_SSB_SCS = sQuery(f':CONF:NR5G:DL:CC1:SSBL1:SSP?')
    FSW_SSB_Pat = sQuery(f':CONF:NR5G:DL:CC1:SSBL1:PATT?')
    FSW_SSB_Off = sQuery(f':CONF:NR5G:DL:CC1:SSBL1:RTO?')
    FSW_SSB_RBO = sQuery(f':CONF:NR5G:DL:CC1:SSBL1:OFFS?')
    FSW_SSB_Aof = sQuery(f':CONF:NR5G:DL:CC1:SSBL1:ASOF?')

s = socket.socket()
s.connect((SMW_IP, 5025))
cell = 1
SMW_FreqBnd = sQuery(f':SOUR1:BB:NR5G:NODE:CELL{cell}:CARD?')
SMW_ChanBnd = sQuery(f':SOUR1:BB:NR5G:NODE:CELL{cell}:CBW?')
SMW_RefPntA = sQuery(f':SOUR1:BB:NR5G:NODE:CELL{cell}:TXBW:POIN?')
SMW_BWPSCS  = sQuery(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{cell}:{dir}:BWP0:SCSP?')
SMW_BWPRB   = sQuery(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{cell}:{dir}:BWP0:RBN?')
SMW_BWPRBO  = sQuery(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{cell}:{dir}:BWP0:RBOF?')
SMW_ChanRB  = sQuery(f':SOUR1:BB:NR5G:SCH:CELL{cell}:SUBF0:USER0:BWP0:ALL{allc}:RBN?')
SMW_ChanRBO = sQuery(f':SOUR1:BB:NR5G:SCH:CELL{cell}:SUBF0:USER0:BWP0:ALL{allc}:RBOF?')
SMW_ChSymb  = sQuery(f':SOUR1:BB:NR5G:SCH:CELL{cell}:SUBF0:USER0:BWP0:ALL{allc}:SYMN?')
SMW_ChSymbO = sQuery(f':SOUR1:BB:NR5G:SCH:CELL{cell}:SUBF0:USER0:BWP0:ALL{allc}:SYM?')

SMW_configT = sQuery(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{cell}:{dir}:BWP0:{ch}:DMTA:CTYP?')
SMW_MapType = sQuery(f':SOUR1:BB:NR5G:SCH:CELL{cell}:SUBF0:USER0:BWP0:ALL0:MAPT?')
SMW_1stAPos = sQuery(f':SOUR1:BB:NR5G:NODE:CELL{cell}:TAP?')
SMW_addPosi = sQuery(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{cell}:{dir}:BWP0:{ch}:DMTA:APIN?')
# SMW_dmrsLen = sQuery(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{cell}:{dir}:BWP0:{ch}:DMTA:MLEN?')
SMW_dmrsLen = sQuery(f':SOUR1:BB:NR5G:SCH:CELL{cell}:SUBF0:USER0:BWP0:ALL0:{ch}:DMRS:LENG?')
SMW_relPowr = sQuery(f':SOUR1:BB:NR5G:SCH:CELL{cell}:SUBF0:USER0:BWP0:ALL0:{ch}:DMRS:POW?')
SMW_MMLayer = sQuery(f':SOUR1:BB:NR5G:SCH:CELL{cell}:SUBF0:USER0:BWP0:ALL0:{ch}:TXSC:NLAY?')
SMW_cdmGrup = sQuery(f':SOUR1:BB:NR5G:SCH:CELL{cell}:SUBF0:USER0:BWP0:ALL0:{ch}:TXSC:CDMD?')
# SSB
if dir == 'DL':
    SMW_SSB_SCS = sQuery(f':SOUR1:BB:NR5G:NODE:CELL{cell}:SSPB0:SCSP?')
    SMW_SSB_Pat = sQuery(f':SOUR1:BB:NR5G:NODE:CELL{cell}:SSPB0:CASE?')
    SMW_SSB_Off = sQuery(f':SOUR1:BB:NR5G:NODE:CELL{cell}:OFFS?')
    SMW_SSB_RBO = sQuery(f':SOUR1:BB:NR5G:NODE:CELL{cell}:SSPB0:RBOF?')
    SMW_SSB_Aof = sQuery(f':SOUR1:BB:NR5G:NODE:CELL{cell}:SSPB0:SCOF?')

print(f'Freq Range :  FSW , SMW ')
print(f'Freq Range : {FSW_FreqBnd:^5},{SMW_FreqBnd:^5}')
print(f'Chan Range : {FSW_ChanBnd:^5},{SMW_ChanBnd:^5}')
print(f'Ref Pnt A  : {FSW_RefPntA:^5},{SMW_RefPntA:^5}')
print(f'-----------: [---BWP---]')
print(f'BWP SCP    : {FSW_BWPSCS:^5},{SMW_BWPSCS:^5}')
print(f'BWP RB     : {FSW_BWPRB:^5},{SMW_BWPRB:^5}')
print(f'BWP RB Offs: {FSW_BWPRBO:^5},{SMW_BWPRBO:^5}')
print(f'-----------: [--PxSCH--]')
print(f'PxSCH RB   : {FSW_ChanRB:^5},{SMW_ChanRB:^5}')
print(f'PxSCH RB Of: {FSW_ChanRBO:^5},{SMW_ChanRBO:^5}')
print(f'PxSCH Sym  : {FSW_ChSymb:^5},{SMW_ChSymb:^5}')
print(f'PxSCH SymOf: {FSW_ChSymbO:^5},{SMW_ChSymbO:^5}')
print(f'-----------: [---DMRS--]')
print(f'Config Type: {FSW_configT:^5},{SMW_configT:^5}')
print(f'1st Mapping: {FSW_MapType:^5},{SMW_MapType:^5}')
print(f'1st Symb   : {FSW_1stAPos:^5},{SMW_1stAPos:^5}')
print(f'Add Positin: {FSW_addPosi:^5},{SMW_addPosi:^5}')
print(f'DMRS Length: {FSW_dmrsLen:^5},{SMW_dmrsLen:^5}')
print(f'Rel Power  : {FSW_relPowr:^5},{SMW_relPowr:^5}')
print(f'-----------: [--MIMO--]')
print(f'MIMO Layers: {FSW_MMLayer:^5},{SMW_MMLayer:^5}')
print(f'CDM Group  : {FSW_cdmGrup:^5},{SMW_cdmGrup:^5}')
if dir == 'DL':
    print(f'-----------: [---SSB---]')
    print(f'SSB SCS    : {FSW_SSB_SCS:^5},{SMW_SSB_SCS:^5}')
    print(f'SSB Pattern: {FSW_SSB_Pat:^5},{SMW_SSB_Pat:^5}')
    print(f'SSB Offset : {FSW_SSB_Off:^5},{SMW_SSB_Off:^5}')
    print(f'SSB RB Off : {FSW_SSB_RBO:^5},{SMW_SSB_RBO:^5}')
    print(f'Add Offset : {FSW_SSB_Aof:^5},{SMW_SSB_Aof:^5}')
