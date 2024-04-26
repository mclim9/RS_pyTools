from iSocket import iSocket                 # Import socket module

林 = iSocket().open('172.24.225.130', 5025)
林.s.settimeout(5)
print(林.query('*IDN?'))

林.tick()
# 林.query('SOUR1:IQ:OUTP:ANAL:STAT ON; *OPC?')
# 林.query('SOUR1:IQ:OUTP:ANAL:STAT OFF;*OPC?')
# 林.query('SOUR1:IQ:OUTP:ANAL:STAT OFF;OUTP1 OFF;*OPC?')
# 林.query('SOUR1:IQ:OUTP:ANAL:STAT ON;OUTP1 ON;*OPC?')
# 林.query('OUTP1 OFF;*OPC?')
# 林.query('OUTP1 ON;*OPC?')
# 林.query('INIT:IMM;*OPC?')
林.query('SOUR1:POW -100;*OPC?')
林.query('SOUR1:POW -10;*OPC?')
林.tock('stuff')
