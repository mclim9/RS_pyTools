from iSocket import iSocket                 # Import socket module

# ## Main Code
fsw = iSocket().open('192.168.1.109', 5025)

fsw.write(':HCOP:CONT HCOP')
fsw.write(':MMEM:NAME "test.png"')
fsw.write(':HCOP:IMM1')
