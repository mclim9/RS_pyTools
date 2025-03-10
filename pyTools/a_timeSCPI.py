from iSocket import iSocket                 # Import socket module

林 = iSocket().open('172.24.225.107', 5025)
林.s.settimeout(5)
print(林.query('*IDN?'))

timeList = []
for i in range(10):
    林.tick()
    林.query('SOUR1:IQ:OUTP:ANAL:STAT OFF;OUTP1 OFF;*OPC?') # RF & IQ
    林.query('SOUR1:IQ:OUTP:ANAL:STAT ON;OUTP1 ON;*OPC?')   # RF & IQ
    # 林.query('SOUR1:IQ:OUTP:ANAL:STAT ON; *OPC?')           # IQ Output
    # 林.query('SOUR1:IQ:OUTP:ANAL:STAT OFF;*OPC?')           # IQ Output
    # 林.query('OUTP1 OFF;*OPC?')                             # RF Output
    # 林.query('OUTP1 ON;*OPC?')                              # RF Output
    # 林.query('INIT:IMM;*OPC?')
    # 林.query('SOUR1:POW -100;*OPC?')
    # 林.query('SOUR1:POW -10;*OPC?')
    timeList.append(林.tock('stuff'))
print(f'AvgTime: {sum(timeList) / len(timeList):5.3f} secs')


instrument.spect.query('SOUR1:IQ:OUTP:ANAL:STAT ON;OUTP1 ON;*OPC?')

instrument.write('SOUR1:IQ:OUTP:ANAL:STAT ON;OUTP1 ON;*OPC?')
instrument.read()

