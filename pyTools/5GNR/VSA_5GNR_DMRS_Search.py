""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module
from iSck_FSW_5GNR_GetSettings import get_5GNR_settings

# #############################################################################
# ## Main Code
# #############################################################################
filename = __file__.split('.py')[0] + '.txt'

fileOut = open(filename, 'a')
FSW = iSocket().open('192.168.58.109', 5025)
FSW.s.settimeout(30)
FSW.write('INIT:CONT OFF')
FSW.write(':SENS:NR5G:FRAM:SLOT 4')                     # Measure 4 slots
fileOut.write(f'{FSW.idn}\n')
fileOut.write(f'{get_5GNR_settings()}\n')
header = 'Config,MapType,APos,addPos,LEN,CDM Group,EVM'
print(header)
fileOut.write(f'{header}\n')

for config in ['1', '2']:                               # DMRS Config Type
    for MapType in ['A', 'B']:                          # DMRS Mapping Type
        for APos in ['2', '3']:                         # DMRS Type A Position
            for addPos in ['0', '1', '2', '3']:         # DMRS Additional Pos
                for dmrsLen in ['1', '2']:              # DMRS Length
                    for cdmGrp in ['1', '2']:           # CDM Group
                        FSW.write(f':CONF:NR5G:DL:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:CTYP {config}')
                        FSW.write(f':CONF:NR5G:DL:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:MTYP {MapType}')
                        if MapType == 'A':
                            FSW.write(f':CONF:NR5G:DL:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:TAP {APos}')
                        FSW.write(f':CONF:NR5G:DL:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:MSYM:APOS {addPos}')
                        FSW.write(f':CONF:NR5G:DL:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:MSYM:LENG {dmrsLen}')
                        FSW.write(f':CONF:NR5G:DL:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:CGWD {cdmGrp}')
                        FSW.query('INIT:IMM;*OPC?')
                        # EVM = FSW.query(':FETC:CC1:ISRC:FRAM:SUMM:EVM:ALL?')      # 1CC All EVM
                        EVM = FSW.query(':TRAC3:DATA? TRACE1').split(',')           # Alloc Summ
                        # EVM = float(EVM[80])          # 0/0/0 PDSCH DMRS0
                        EVM = float(EVM[116])           # 0/0/1 PDSCH DMRS0
                        data = f'{config},{MapType},{APos},{addPos},{dmrsLen},{cdmGrp},{EVM:7.3f}'
                        if EVM < 10:
                            print(data)
                        fileOut = open(filename, 'a')
                        fileOut.write(f'{data}\n')
                        fileOut.close()
