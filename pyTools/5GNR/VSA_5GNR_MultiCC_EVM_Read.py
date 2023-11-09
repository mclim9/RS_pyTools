""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

# #############################################################################
# ## Main Code
# #############################################################################
FSW = iSocket().open('192.168.58.109', 5025)

arry = []
numCC = FSW.queryInt(f':CONF:NR5G:NOCC?')
for i in range(numCC):
    averg = FSW.queryFloat(f':FETC:CC{i+1}:SUMM:EVM:ALL:AVER?')     # DMRS + Phy Ch
    PEAK  = FSW.queryFloat(f':FETC:CC{i+1}:SUMM:EVM:PEAK:AVER?')    # peak
    PxSCH = FSW.queryFloat(f':FETC:CC{i+1}:SUMM:EVM:PCH:AVER?')     # Phy ch
    DMRS  = FSW.queryFloat(f':FETC:CC{i+1}:SUMM:EVM:PSIG:AVER?')    # DMRS
    arry.append(averg)
    print(f'CC{i+1}, {averg:7.3f}, {PxSCH:7.3f}, {DMRS:7.3f}')

evmMin = min(arry)
evmMax = max(arry)
print(f'{evmMin}, {evmMax}, {evmMax - evmMin}')