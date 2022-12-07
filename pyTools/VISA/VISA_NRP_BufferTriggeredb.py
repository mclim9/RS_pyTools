""" Rohde & Schwarz Automation for demonstration use.

    SMW BB-A Marker --> User1
    User1:
        --> Inst Trg A
        --> NRP-Ext2

    List Mode : Extern Step
"""

import pyvisa as visa

numMeas = 17

def vQuery(SCPI):                           # Socket Query
    sOut = instr.query(SCPI).strip()
    print(f'Query: {sOut}')
    return sOut

def vWrite(SCPI):                           # Socket Write
    print(f'Write: {SCPI}')
    instr.write(SCPI)

def nrpClrError():
    ErrList = []
    while True:
        RdStr = vQuery("SYST:ERR?").strip()
        ErrList.append(RdStr)
        RdStrSplit = RdStr.split(',')
        if RdStr == "<notRead>":
            break                           # No readstring
        if RdStrSplit[0] == "0":
            break                           # Read 0 error:R&S
    return ErrList

def Get_Power():
    vWrite('UNIT:POW DBM;:INIT:IMM')
    outp = vQuery('FETCH?')
    return outp

rm = visa.ResourceManager()
instr = rm.open_resource(f'USB::0x0AAD::0x015F::101467::INSTR')
instr.timeout = 5000

# vQuery(f'*RST;*OPC?')
szBuff = nrpClrError()                          # Clear error queue
vQuery(f'*IDN?')
vWrite('SENS:AVER:COUN:AUTO OFF')               # Auto Averaging OFF
vWrite('SENS:AVER:COUN 4')                      # Avg Count = 4
vWrite('SENS:POW:AVG:APER 10e-6')               # Aperture
vWrite('TRIG:SOUR EXT2')                        # external input (SMB-type connector)

vWrite('TRIG:ATR:STAT OFF')                     # Auto-Trigger OFF
vWrite(f'SENS:POW:AVG:BUFF:SIZE {numMeas}')     # Buffer size = 17
vWrite('SENS:POW:AVG:BUFF:STAT ON')             # Configure buffered measurement
vWrite('SENS:POW:AVG:BUFF:CLE')                 # Clear buffer
# vWrite(f'SENS:TRAC:POINT {numMeas}')
vWrite(f'TRIG:COUN {numMeas}')
szBuff = nrpClrError()                          # Clear error queue

vWrite('STAT:OPER:MEAS:NTR 2')
vWrite('STAT:OPER:MEAS:PTR 0')

nrpData = Get_Power().split(',')
print(f'#Data: {len(nrpData)}')
