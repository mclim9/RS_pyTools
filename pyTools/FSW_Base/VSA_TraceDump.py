""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                     # Import socket module

def main():
    FSW = iSocket().open('192.168.58.109', 5025)
    FileOut = FSW.logging_test('VSA_Trace.csv')
    FileOut.info(f'{FSW.idn}')

    FSW.timeout(5)
    # FSW.write(':INST:SE#L "Spectrum"')        # Select Analog Demod
    FSW.write(':INIT:CONT OFF')                 # Single Sweep
    FSW.write(':FORM:DATA ASCII')               # ASCII Output

    chunk = 500
    trace = ''
    points = FSW.queryInt(':SENS:SWE:WIND:POIN?')   # Spectrum
    points = FSW.queryInt(':SENS4:SWE:LENG?')       # K18
    tracAM = FSW.query(':TRAC4:DATA? TRACE1')

    for i in range(points // chunk):
        rdChunk  = FSW.query(f'TRAC:DATA:MEM? TRACE1,{i * chunk},{chunk}')
        if len(rdChunk) < chunk * 18 - 1:
            rdChunk  = FSW.query(f'TRAC:DATA:MEM? TRACE1,{i * chunk},{chunk}')
            print(f'reread chunk{i}')
        trace += rdChunk + ','

    print(f'Points: {len(trace.split(","))}')
    FileOut.info(f'{trace}')
    FileOut.info(f'Points: {len(trace.split(","))}')

if __name__ == "__main__":
    main()
