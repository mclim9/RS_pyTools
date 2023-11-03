""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                         # Import socket module

def config_system():
    fsw.write(':INIT:CONT OFF')
    fsw.write(':LAY:REM:WIND "4"')
    fsw.query(':LAY:ADD:WIND? "1",RIGH,PFPPdu')
    global monkey
    monkey = fsw.logging_test(__file__ + '.log')

if __name__ == "__main__":
    fsw = iSocket().open('192.168.58.109', 5025)    # fsw = FSW
    smw = iSocket().open('192.168.58.114', 5025)    # smw = SMW
    config_system()
    print('Freq:MHz, PPDU Typ,   Bytes, Tim:uSec,      EVM,  ChEst, Time:Sec')
    for size in range(10):
        smw.write(f':SOUR1:BB:WLNN:FBL1:USER1:MPDU1:COUN {size+1}')
        for j in range(size + 1):
            smw.query(f':SOUR1:BB:WLNN:FBL1:USER1:MPDU{j+1}:DATA:LENG 16000;*OPC?')
        time_array = []
        for i in range(10):
            fsw.tick()
            fsw.query('INIT:IMM;*OPC?')
            time_array.append(fsw.tock())

        TTime = sum(time_array) / len(time_array)
        Lengt = smw.queryInt(':SOUR1:BB:WLNN:FBL1:USER1:DATA:LENG?')
        CTime = (Lengt) / 160
        Freq  = fsw.queryFloat(':SENS:FREQ:CENT?')
        PPDU  = fsw.query('FETC:BURS:PPDU:TYPE?')
        EVM   = fsw.query(':FETC:BURS:EVM:ALL:AVER?').split(',')[0]
        ChEst = fsw.query(':SENS:DEM:CEST:RANG?')
        月明 = f'{Freq/1e6:7.3f}, {PPDU}, {Lengt:7}, {CTime:8.3f}, {EVM}, {ChEst:6}, {TTime:5.3f}'
        print(月明)
        monkey.info(f'{月明}')
