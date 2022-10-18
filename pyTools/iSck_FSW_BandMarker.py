from iSocket import iSocket                 # Import socket module

# ## Main Code
fsw = iSocket().open('192.168.58.109', 5025)

fsw.write('*RST')
fsw.write('*CLS')
fsw.write(':SYST:DISP:UPD ON')
fsw.write(':INIT:CONT OFF')
fsw.write(':CALC:MARK:FUNC:NDBD:STAT ON')
fsw.write(':CALC:MARK:FUNC:NDBD 20.00 dB')
fsw.query('INIT:IMM; *OPC?')
test = fsw.query(':CALC:MARK:FUNC:NDBD:FREQ?')
test = test.split(',')                              # Split string
frq1 = float(test[0])
frq2 = float(test[1])
if frq2 - frq1 > 1e9:
    data = 0                                        # do nothing
else:
    data = fsw.query(':CALC:MARK:FUNC:NDBD:RES?')
fsw.write(':INIT:CONT ON')
fsw.write(':SYST:ERR?')

print(data)
