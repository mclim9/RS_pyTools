from iSocket import iSocket                               # Import socket module
import timeit

def timeSCPI(SCPI_In):
    tick = timeit.default_timer()
    s.query(SCPI_In)
    print(f'TTime: {timeit.default_timer() - tick:.6f}sec {SCPI_In}')

def main():
    s.write('SYST:DISP:UPD ON')
    s.write('INIT:CONT OFF')

    timeSCPI('*IDN?')                       # Baseline speed
    timeSCPI(':INIT:IMM;*OPC?')             # Used by VSA
    # timeSCPI(':INIT:IMM:ALL;*OPC?')       # Used by VNA

    s.clear_error()
    s.close

if __name__ == '__main__':
    s = iSocket().open('172.24.225.101', 5025)
    main()
