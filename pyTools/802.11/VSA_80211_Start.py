""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                             # Import socket module

FSW = iSocket().open('192.168.58.109', 5025)
SMW = iSocket().open('192.168.58.114', 5025)
FSW.timeout(30)                                         # Timeout in seconds

def main():
    SMW.write(':OUTP:STAT 1')
    FSW.write(':INIT:CONT OFF')                         # Single sweep
    FSW.write(':INIT:IMM')
    FSW.delay(5)
    SMW.write(':OUTP:STAT 0')
    print('Stop SMW')
    FSW.write(':INIT:IMM')

if __name__ == "__main__":
    main()
