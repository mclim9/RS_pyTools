""" Rohde & Schwarz Automation for demonstration use."""
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

print(f'IDN:{vQuery(f"*IDN?")} {Get_Power()}')
vQuery(f'*IDN?')
