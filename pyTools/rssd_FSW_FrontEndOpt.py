""" Rohde & Schwarz Automation for demonstration use."""
from rssd.instrument import instr
scpiEVM = 'FETC:CC1:ISRC:FRAM:SUMM:EVM:ALL:AVER?'
scpiPWR = 'FETC:SUMM:POW?'

def get_stats():
    reflvl  = FSW.queryFloat('DISP:TRAC:Y:RLEV?')
    preamp  = FSW.query('INP:GAIN:STAT?')
    attn    = FSW.queryInt('INP:ATT?')
    chPwr   = FSW.queryFloat(scpiPWR)
    evm     = FSW.queryFloat(scpiEVM)
    print(f'{reflvl:.3f},{preamp},{attn},{chPwr:.3f},{evm:.3f}')
    return [reflvl, preamp, attn, chPwr, evm]

def get_overload():
    FSW.query('INIT:IMM;*OPC?')
    reg = FSW.queryInt('STAT:QUES:POW:COND?')
    return reg

def optimizeAttn():
    FSW.write('INIT:CONT OFF')
    while get_overload() < 1:
        stats = get_stats()
        attn = stats[2]
        if attn == 0:
            break
        FSW.write(f'INP:ATT {attn -1}')
    FSW.write(f'INP:ATT {attn}')
    return stats

def optimizeRefLvl():
    FSW.write('INIT:CONT OFF')
    startRef = get_stats()[0]
    while get_overload() < 1:
        refL = get_stats()[0]
        if (startRef - refL) > 10:
            break
        FSW.write(f'DISP:TRAC:Y:RLEV {refL - 1}')
    FSW.write(f'DISP:TRAC:Y:RLEV {refL}')

# #########################################################
# ## Main Code
# #########################################################
FSW = instr().open('192.168.58.109', 'hislip')

FSW.write(':SYST:PASS:CEN "894129"')
FSW.write('DIAG:SERV:SFUN "2.0.46.0.0"')
FSW.write('ADJ:LEV')
stats = get_stats()

attnStats = optimizeAttn()
if stats[1] == '1':                         # If Preamp ON
    FSW.query('INP:GAIN:STAT OFF;*OPC?')    # Preamp Off
    FSW.query('INIT:IMM;*OPC?')
    paoffStats = optimizeAttn()
optimizeRefLvl()
