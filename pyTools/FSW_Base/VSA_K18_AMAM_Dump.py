""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                     # Import socket module

def main():
    FSW = iSocket().open('192.168.1.109', 5025)
    FileOut = FSW.logging_test('VSA_K18_AMAM_Trace.csv')
    FileOut.info(f'{FSW.idn}')
    FSW.timeout(10)

    FSW.write(':INIT:CONT OFF')                 # Single Sweep
    FSW.write(':FORM:DATA ASCII')               # ASCII Output

    points = FSW.queryInt(':SENS4:SWE:LENG?')
    tracAM = FSW.query(':TRAC4:DATA? TRACE1')

    tracLen = len(tracAM.split(","))

    print(f'Points: {tracLen}')
    FileOut.info(f'{tracAM}')
    FileOut.info(f'Points: {tracLen}')

if __name__ == "__main__":
    main()
