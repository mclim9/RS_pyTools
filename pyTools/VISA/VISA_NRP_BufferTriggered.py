""" Rohde & Schwarz Automation for demonstration use."""
import pyvisa as visa
numMeas = 17

def vQuery(SCPI):                           # Socket Query
    vWrite(SCPI)
    sOut = instr.query(SCPI).strip()
    # sOut = "<notRead>"
    print(f'Query: {sOut}')
    return sOut

def vWrite(SCPI):                           # Socket Write
    print(f'Write: {SCPI}')
    instr.write(SCPI)

def nrpClrError():
    ErrList = []
    try:                                                        # Instrument supports SYST:ERR?
        while True:
            RdStr = vQuery("SYST:ERR?").strip()
            ErrList.append(RdStr)
            RdStrSplit = RdStr.split(',')
            if RdStr == "<notRead>": break                     # No readstring
            if RdStrSplit[0] == "0": break                     # Read 0 error:R&S
    except:
        pass
    return ErrList

def Get_Power():
    vWrite('UNIT:POW DBM')
    vWrite(':INIT:IMM')
    outp = vQuery('FETCH?')
    return outp

rm = visa.ResourceManager()
instr = rm.open_resource(f'USB::0x0AAD::0x015F::101467::INSTR')
instr.timeout = 5000

asdf = Get_Power()
# szBuff = nrpClrError()                        # Read out all errors / Clear error queue
vQuery(f'*IDN?')
vWrite('SENS:AVER:COUN:AUTO OFF')               # Auto Averaging OFF
vWrite('SENS:AVER:COUN 4')                      # Avg Count = 4
vWrite('TRIG:SOUR EXT2')                        # external input (SMB-type connector)

vWrite('TRIG:ATR:STAT OFF')                     # Auto-Trigger OFF
vWrite(f'SENS:POW:AVG:BUFF:SIZE {numMeas}')     # Buffer size is randomly selected to 17
vWrite('SENS:POW:AVG:BUFF:STAT ON')             # Configure a buffered measurement
vWrite(f'TRIG:COUN {numMeas}')
# szBuff = nrpClrError()                        # Read out all errors / Clear error queue

vWrite('INIT:IMM')                              # Start a 'single' buffered measurement
vWrite('STAT:OPER:MEAS:NTR 2')                  # The end of a physical measurement can be recognized
vWrite('STAT:OPER:MEAS:PTR 0')                  # by a transistion to 'NOT MEASURING' which is a
for i in range(numMeas):                        # Collect 17 physical measurements
    iDummy = vQuery('STAT:OPER:MEAS:EVEN?')     # Clear the event register by reading it

    # if (bUseBUSTrigger):                      # SW '*TRG' if SMB HW not connected
    #     vWrite('*TRG')

    evntFlag = 0
    while (evntFlag != 2):                      # Loop until the measurement is done
        evntFlag = vQuery('STAT:OPER:MEAS:EVEN?')
        evntFlag = int(evntFlag) & 2
    print('Triggered!\n')                       # All 17 physical measurement have been executed.

nrpData = vQuery('FETCH?')
print(nrpData)
