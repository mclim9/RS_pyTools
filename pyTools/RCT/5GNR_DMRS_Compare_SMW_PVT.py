""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

PVT = iSocket().open('192.168.58.30', 5025)
SMW = iSocket().open('192.168.58.114', 5025)
PVT.s.settimeout(1)
dir = 'UL'  # UL | DL
if dir == 'DL':
    allc = 1
    ch  = 'PDSC'
else:
    allc = 0
    ch  = 'PUSC'

PVT_FreqBnd = 'Nope'
PVT_ChanBnd = PVT.query(f':CONF:NRS:MEAS1:CC1:CBAN?')
BWP = PVT.query(f':CONF:NRS:MEAS:CC1:BWP? BWP0').split(',')
PVT_BWPSCS  = BWP[0]
PVT_BWPRB   = BWP[2]
PVT_BWPRBO  = BWP[3]
# --------------
PVT_PUSCH  = PVT.query(f'CONF:NRS:MEAS:CC1:ALL1:PUSC?').split(',')
PVT_MapType = PVT_PUSCH[0]
PVT_ChSymb  = PVT_PUSCH[1]
PVT_ChSymbO = PVT_PUSCH[2]
PVT_ChanRB  = PVT_PUSCH[4]
PVT_ChanRBO = PVT_PUSCH[5]
PVT_Modulat = PVT_PUSCH[6]

PVT_1stAPos = PVT.query(f'CONF:NRS:MEAS1:CC1:TAP?')
PVT_DMRS_A  = PVT.query(f'CONF:NRS:MEAS1:CC1:BWP:PUSC:DMTA? BWP0').split(',')
PVT_configT = PVT_DMRS_A[0]
PVT_addPosi = PVT_DMRS_A[1]
PVT_dmrsLen = PVT_DMRS_A[2]

PVT_cdmGrup = PVT.query(f'CONF:NRS:MEAS1:CC1:ALL1:PUSC:ADD?').split(',')
PVT_relPowr = 'nope'
PVT_MMLayer = PVT.query(f'CONF:NRS:MEAS1:CC1:ALL1:PUSC:NLAY?')
PVT_dmrsLen = PVT_cdmGrup[0]
PVT_AntPort = PVT_cdmGrup[1]
PVT_cdmGrup = PVT_cdmGrup[2]

SMW_FreqBnd = SMW.query(f':SOUR1:BB:NR5G:NODE:CELL0:CARD?')
SMW_ChanBnd = SMW.query(f':SOUR1:BB:NR5G:NODE:CELL0:CBW?')
SMW_BWPSCS  = SMW.query(f':SOUR1:BB:NR5G:UBWP:USER0:CELL0:{dir}:BWP0:SCSP?')
SMW_BWPRB   = SMW.query(f':SOUR1:BB:NR5G:UBWP:USER0:CELL0:{dir}:BWP0:RBN?')
SMW_BWPRBO  = SMW.query(f':SOUR1:BB:NR5G:UBWP:USER0:CELL0:{dir}:BWP0:RBOF?')
SMW_ChanRB  = SMW.query(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL{allc}:RBN?')
SMW_ChanRBO = SMW.query(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL{allc}:RBOF?')
SMW_ChSymb  = SMW.query(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL{allc}:SYMN?')
SMW_ChSymbO = SMW.query(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL{allc}:SYM?')
SMW_Modulat = SMW.query(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL{allc}:MOD?')

SMW_configT = SMW.query(f':SOUR1:BB:NR5G:UBWP:USER0:CELL0:{dir}:BWP0:{ch}:DMTA:CTYP?')
SMW_MapType = SMW.query(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:MAPT?')
SMW_1stAPos = SMW.query(f':SOUR1:BB:NR5G:NODE:CELL0:TAP?')
SMW_addPosi = SMW.query(f':SOUR1:BB:NR5G:UBWP:USER0:CELL0:{dir}:BWP0:{ch}:DMTA:APIN?')
SMW_dmrsLen = SMW.query(f':SOUR1:BB:NR5G:UBWP:USER0:CELL0:{dir}:BWP0:{ch}:DMTA:MLEN?')
SMW_relPowr = SMW.query(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:{ch}:DMRS:POW?')
SMW_MMLayer = SMW.query(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:{ch}:TXSC:NLAY?')
SMW_cdmGrup = SMW.query(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:{ch}:TXSC:CDMD?')


print(f'Freq Range :  PVT , SMW ')
print(f'Freq Range : {PVT_FreqBnd:^5},{SMW_FreqBnd:^5}')
print(f'Chan Range : {PVT_ChanBnd:^5},{SMW_ChanBnd:^5}')
print(f'BWP SCP    : {PVT_BWPSCS:^5},{SMW_BWPSCS:^5}')
print(f'BWP RB     : {PVT_BWPRB:^5},{SMW_BWPRB:^5}')
print(f'BWP RB Offs: {PVT_BWPRBO:^5},{SMW_BWPRBO:^5}')
print(f'PxSCH RB   : {PVT_ChanRB:^5},{SMW_ChanRB:^5}')
print(f'PxSCH RB Of: {PVT_ChanRBO:^5},{SMW_ChanRBO:^5}')
print(f'PxSCH Sym  : {PVT_ChSymb:^5},{SMW_ChSymb:^5}')
print(f'PxSCH SymOf: {PVT_ChSymbO:^5},{SMW_ChSymbO:^5}')
print(f'PxSCH SymOf: {PVT_Modulat:^5},{SMW_Modulat:^5}')
print(f'-----------: -----,-----')
print(f'Config Type: {PVT_configT:^5},{SMW_configT:^5}')
print(f'1st Mapping: {PVT_MapType:^5},{SMW_MapType:^5}')
print(f'1st Symb   : {PVT_1stAPos:^5},{SMW_1stAPos:^5}')
print(f'Add Positin: {PVT_addPosi:^5},{SMW_addPosi:^5}')
print(f'DMRS Length: {PVT_dmrsLen:^5},{SMW_dmrsLen:^5}')
print(f'Rel Power  : {PVT_relPowr:^5},{SMW_relPowr:^5}')
print(f'-----------: -----,-----')
print(f'MIMO Layers: {PVT_MMLayer:^5},{SMW_MMLayer:^5}')
print(f'Ant Port   : {PVT_AntPort:^5},n/a')
print(f'CDM Group  : {PVT_cdmGrup:^5},{SMW_cdmGrup:^5}')
