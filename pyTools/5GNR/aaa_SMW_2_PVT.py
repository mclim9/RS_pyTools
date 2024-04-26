""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

SMW_IP = '172.24.225.130'
PVT_IP = '172.24.225.107'

SMW = iSocket().open(SMW_IP, 5025)
PVT = iSocket().open(PVT_IP, 5025)

def Config_SMW():
    Band = SMW.query(':SOUR1:BB:NR5G:NODE:CELL0:CARD?')
    Dir  = SMW.query(':SOUR1:BB:NR5G:LINK?')
    BW   = SMW.query(':SOUR1:BB:NR5G:NODE:CELL0:CBW?')
    if Dir == 'UP':
        allc = 0
        dir  = 'UL'
        ch  = 'PUSC'
    elif Dir == 'DOWN':
        allc = 1
        dir  = 'DL'
        ch  = 'PDSC'

    SCS  = SMW.query(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:DL:BWP0:SCSP?')
    Mod  = SMW.query(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL{allc}:MOD?')
    RBN  = SMW.query(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL{allc}:RBN?')

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
    SMW.clear_error()

    Wavename = f'{Band}_{dir}_{SCS}SCS_{BW}_{RBN}RB_{Mod}'
    print(f'{Wavename}')

def Config_PVT():
    PVT.query(f'*IDN?')

    PVT.query(f'CONF:NRS:MEAS:CC1:CBAN {SMW_ChanBnd.replace("BW", "B")};*OPC?')
    PVT.query(f'CONF:NRS:MEAS:CC1:PLC {0};*OPC?')
    PVT.query(f'CONF:NRS:MEAS:CC1:TAP {SMW_1stAPos};*OPC?')

    if "N" in SMW_BWPSCS:
        CP = 'NORM'
    else:
        CP = 'EXT'
    SCS = int(SMW_BWPSCS.replace('N','0'))
    PVT.query(f'CONF:NRS:MEAS:CC1:BWP BWP0,S{SCS}K,{CP},{SMW_BWPRB},{SMW_BWPRBO};*OPC?')
    PVT.clear_error()

if __name__ == "__main__":
    Config_SMW()
    Config_PVT()

