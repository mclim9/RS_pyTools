import os
import timeit
from iSocket import iSocket                                         # Import socket module

def readIni(file):
    path = os.path.dirname(__file__)
    iniFile = open(f'{path}\\{file}', 'r')
    lines = iniFile.readlines()
    data = []
    for line in lines:
        if ' = ' in line:
            data.append(line.split(' = ')[1].strip())
    return data

def readSwitchCount():
    AC_DC = FSW.queryInt('DIAG:INFO:CCO? ACDC')
    Attn5 = FSW.queryInt('DIAG:INFO:CCO? ATT5')
    Attn10 = FSW.queryInt('DIAG:INFO:CCO? ATT10')
    Attn20 = FSW.queryInt('DIAG:INFO:CCO? ATT20')
    Attn40 = FSW.queryInt('DIAG:INFO:CCO? ATT40')
    CalSrc = FSW.queryInt('DIAG:INFO:CCO? CAL')
    Preamp = FSW.queryInt('DIAG:INFO:CCO? PRE')
    total = AC_DC + Attn5 + Attn10 + Attn20 + Attn40 + CalSrc + Preamp
    return total

def readEVM():
    FSW.query('ADJ:LEV;*OPC?')
    FSW.query('INIT:IMM;*OPC?')
    EVM = FSW.queryFloat('FETC:SUMM:EVM:ALL:AVER?')

def readACLR():
    FSW.query('ADJ:LEV;*OPC?')
    FSW.query('INIT:IMM;*OPC?')
    ACLR = FSW.query(':CALC:MARK:FUNC:POW:RES? ACP').split(',')
    ACLR = float(ACLR[1])
    # print(f'ACLR:{ACLR:.3f} SWNum:{SWNum:02d} Time:{timeit.default_timer() - tick:.3f}')

if __name__ == "__main__":
    FSW = iSocket().open('192.168.58.109', 5025)
    SMW = iSocket().open('192.168.58.114', 5025)

    data = readIni('iSck_FSW_MMO_ACLR.ini')
    FSW.write(':INIT:CONT OFF')
    FSW.write(':SYST:PASS:CEN "894129"')
    y = int(float(data[0]))
    x = int(float(data[1]))
    z = int(float(data[2]))
    w = int(float(data[3])) + 15
    k = int(float(data[4])) + 30

    SWStart = readSwitchCount()
    tick = timeit.default_timer()
    for i in range(-50, 0, 1):
        FSW.write(f'DIAG:SERV:SFUN "2.0.46.1.4.1.20.{y:.0f}.{x:.0f}.{z:.0f}.{w:.0f}.{k:.0f}"')
        FSW.write('DIAG:SERV:SFUN "2.0.46.0.1"')              # MMO On
        # FSW.write(f'DIAG:SERV:SFUN "2.0.46.1.4.1.20.{y:.0f}.{x:.0f}.{z:.0f}.{w:.0f}.{k:.0f}"')
        SMW.write(f'SOUR1:POW:POW {i}')
        # readEVM()
        readACLR()
    SWStop = readSwitchCount()
    print(f'SWNum:{SWStop - SWStart:02d} Time:{timeit.default_timer() - tick:.3f}')

    SWStart = readSwitchCount()
    tick = timeit.default_timer()
    for i in range(-50, 0, 1):
        FSW.write('DIAG:SERV:SFUN "2.0.46.0.0"')              # MMO Off
        SMW.write(f'SOUR1:POW:POW {i}')
        # readEVM()
        readACLR()
    SWStop = readSwitchCount()
    print(f'SWNum:{SWStop - SWStart:02d} Time:{timeit.default_timer() - tick:.3f}')

# -19.-61.-13.-8.1
