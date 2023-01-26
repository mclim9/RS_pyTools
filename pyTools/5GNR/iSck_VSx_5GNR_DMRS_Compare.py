""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

FSW = iSocket().open('192.168.58.109', 5025)
SMW = iSocket().open('192.168.58.114', 5025)
FSW.s.settimeout(1)
dir = 'UL'  # UL | DL
if dir == 'DL':
    allc = 1
    ch  = 'PDSC'
else:
    allc = 0
    ch  = 'PUSC'

FSW.query('INIT:IMM;*OPC?')
FSW_FreqBnd = FSW.query(f':CONF:NR5G:{dir}:CC1:DFR?')
FSW_ChanBnd = FSW.query(f':CONF:NR5G:{dir}:CC1:BW?')
FSW_BWPSCS  = FSW.query(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SSP?')
FSW_BWPRB   = FSW.query(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:RBC?')
FSW_BWPRBO  = FSW.query(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:RBOF?')
FSW_ChanRB  = FSW.query(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:RBC?')
FSW_ChanRBO = FSW.query(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:RBOF?')
FSW_ChSymb  = FSW.query(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:SCO?')
FSW_ChSymbO = FSW.query(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:SOFF?')
# --------------
FSW_configT = FSW.query(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:CTYP?')
FSW_MapType = FSW.query(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:MTYP?')
FSW_1stAPos = FSW.query(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:TAP?')
FSW_addPosi = FSW.query(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:MSYM:APOS?')
FSW_dmrsLen = FSW.query(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:MSYM:LENG?')
FSW_relPowr = FSW.query(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:POW?')
FSW_MMLayer = FSW.query(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:CLM?')
FSW_cdmGrup = FSW.query(f':CONF:NR5G:{dir}:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:CGWD?')

SMW_FreqBnd = SMW.query(f':SOUR1:BB:NR5G:NODE:CELL0:CARD?')
SMW_ChanBnd = SMW.query(f':SOUR1:BB:NR5G:NODE:CELL0:CBW?')
SMW_BWPSCS  = SMW.query(f':SOUR1:BB:NR5G:UBWP:USER0:CELL0:{dir}:BWP0:SCSP?')
SMW_BWPRB   = SMW.query(f':SOUR1:BB:NR5G:UBWP:USER0:CELL0:{dir}:BWP0:RBN?')
SMW_BWPRBO  = SMW.query(f':SOUR1:BB:NR5G:UBWP:USER0:CELL0:{dir}:BWP0:RBOF?')
SMW_ChanRB  = SMW.query(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL{allc}:RBN?')
SMW_ChanRBO = SMW.query(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL{allc}:RBOF?')
SMW_ChSymb  = SMW.query(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL{allc}:SYMN?')
SMW_ChSymbO = SMW.query(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL{allc}:SYM?')

SMW_configT = SMW.query(f':SOUR1:BB:NR5G:UBWP:USER0:CELL0:{dir}:BWP0:{ch}:DMTA:CTYP?')
SMW_MapType = SMW.query(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:MAPT?')
SMW_1stAPos = SMW.query(f':SOUR1:BB:NR5G:NODE:CELL0:TAP?')
SMW_addPosi = SMW.query(f':SOUR1:BB:NR5G:UBWP:USER0:CELL0:{dir}:BWP0:{ch}:DMTA:APIN?')
SMW_dmrsLen = SMW.query(f':SOUR1:BB:NR5G:UBWP:USER0:CELL0:{dir}:BWP0:{ch}:DMTA:MLEN?')
SMW_relPowr = SMW.query(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:{ch}:DMRS:POW?')
SMW_MMLayer = SMW.query(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:{ch}:TXSC:NLAY?')
SMW_cdmGrup = SMW.query(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:{ch}:TXSC:CDMD?')


print(f'Freq Range :  FSW , SMW ')
print(f'Freq Range : {FSW_FreqBnd:^5},{SMW_FreqBnd:^5}')
print(f'Chan Range : {FSW_ChanBnd:^5},{SMW_ChanBnd:^5}')
print(f'BWP SCP    : {FSW_BWPSCS:^5},{SMW_BWPSCS:^5}')
print(f'BWP RB     : {FSW_BWPRB:^5},{SMW_BWPRB:^5}')
print(f'BWP RB Offs: {FSW_BWPRBO:^5},{SMW_BWPRBO:^5}')
print(f'PxSCH RB   : {FSW_ChanRB:^5},{SMW_ChanRB:^5}')
print(f'PxSCH RB Of: {FSW_ChanRBO:^5},{SMW_ChanRBO:^5}')
print(f'PxSCH Sym  : {FSW_ChSymb:^5},{SMW_ChSymb:^5}')
print(f'PxSCH SymOf: {FSW_ChSymbO:^5},{SMW_ChSymbO:^5}')
print(f'-----------: -----,-----')
print(f'Config Type: {FSW_configT:^5},{SMW_configT:^5}')
print(f'1st Mapping: {FSW_MapType:^5},{SMW_MapType:^5}')
print(f'1st Symb   : {FSW_1stAPos:^5},{SMW_1stAPos:^5}')
print(f'Add Positin: {FSW_addPosi:^5},{SMW_addPosi:^5}')
print(f'DMRS Length: {FSW_dmrsLen:^5},{SMW_dmrsLen:^5}')
print(f'Rel Power  : {FSW_relPowr:^5},{SMW_relPowr:^5}')
print(f'-----------: -----,-----')
print(f'MIMO Layers: {FSW_MMLayer:^5},{SMW_MMLayer:^5}')
print(f'CDM Group  : {FSW_cdmGrup:^5},{SMW_cdmGrup:^5}')
