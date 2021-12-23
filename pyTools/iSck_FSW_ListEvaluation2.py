""" Rohde & Schwarz Automation for demonstration use."""
import timeit
import socket
import time

class iSocket():
    """ instrument socket class """
    def __init__(self):
        self.s = socket.socket()                    # Create a socket

    def open(self, host, port):                     # noqa: E302
        try:
            self.s.connect((host, port))
            self.s.settimeout(1)                    # Timeout(seconds)
            self.idn = self.query('*IDN?')
            print(f'IDN  : {self.idn}')
        except socket.error:
            print(f"SckErr: {socket.error}")
        return self

    def write(self, SCPI):                          # noqa: E302
        # print(f'iSckt> {SCPI}  ')
        self.s.sendall(f'{SCPI}\n'.encode())        # Write 'SCPI'

    def query(self, SCPI):
        tick = timeit.default_timer()
        self.write(SCPI)
        # time.sleep(.001)
        print(f'Write: {timeit.default_timer() - tick:.6f}sec')
        sOut = self.read()
        print(f'Query: {timeit.default_timer() - tick:.6f}sec')
        return sOut

    def read(self):
        try:
            sOut = self.s.recv(10000000).strip()    # Read socket
            sOut = sOut.decode()
        except socket.error:
            sOut = '<not Read>'
        # print(f'iSckt< {sOut}')
        return sOut

    def timeout(self, seconds):
        self.s.settimeout(seconds)


def validateData(dataArry):
    outStr = ''
    for i, meas in enumerate(dataArry):
        try:
            curr = float(dataArry[i])
            nxt1 = float(dataArry[i + 1])
            delt = int(round(nxt1 - curr))
            outStr += f'{delt}:'
        except IndexError:
            pass
        except Exception as ex:
            print(f"Excepetion: {type(ex).__name__} Arg:\n{ex.args}")
    # print(outStr)
    return outStr


# #############################################################################
# ## Main Code
# #############################################################################
SMW = iSocket().open('192.168.58.114', 5025)
FSW = iSocket().open('192.168.58.109', 5025)
FSW.timeout(10)
SMWClk = 2000
WvSamp = 10000
Points = 20
MeasTime = 200e-6

SMW.write(':SOUR1:BB:ARB:WAV:SEL "/var/user/listmode/SquareMarker"')
# SMW.write(':SOUR1:BB:ARB:TRIG:SEQ SING')            # Single play
SMW.write(f':SOUR1:BB:ARB:CLOC {SMWClk}')
SMW.write(':OUTP1:TM1:SIGN MARKA1')
SMW.write(':SOUR1:BB:ARB:STAT 1')
SMW.write(':SOUR1:IQ:STATe 0')                      # IQ Mod

SMW.write(':OUTP1:STAT 1')
SMW.write(':SOUR1:LIST:SEL "/var/user/listmode/listmode_pwrSweep"')
SMW.write(':SOUR1:LIST:MODE STEP')                  # Step per trigger
SMW.write(':SOUR1:LIST:TRIG:SOUR EXT')              # External trigger
SMW.write(':SOUR1:FREQ:MODE LIST')                  # List mode on
SMW.write(':SOUR1:LIST:RES')                        # Reset List

FSW.write(':INST:SEL "SPECTRUM"')                   # Select Analog Demod
FSW.write(':INIT:CONT OFF')                         # Cont Sweep Off
FSW.write("LIST:POW:SET OFF,ON,OFF,EXT,POS,0,0")    # PkPwr, RMS, Avg, TrgSource, TrgSlope,TrgOffset, GateLen

FSW.write('FORM:DATA REAL,32')
# FSW.write('FORMAT:DATA ASCII')
for SMWClk in [500, 1000, 2000, 3000, 4000]:
    for Points in [20, 40, 60, 100, 200]:
        SMW.query(f':SOUR1:BB:ARB:CLOC {SMWClk};*OPC?')
        freqs = ['1GHz'] * Points                           # freqs
        lst = []
        for freq in freqs:
            cmd = f'{freq},0,10,OFF,NORM,3MHZ,3MHZ,{MeasTime},0' # Freq; RLvl; Attn; EAttn; Filter, RBW, VBW, MeasTime, TrgrLvl
            lst.append(cmd)
        lstcmd = "LIST:POW? " + ','.join(lst)

        SMW.write(':SOUR1:BB:ARB:TRIG:EXEC')                # SMW start trigger
        tick = timeit.default_timer()
        val = FSW.query(lstcmd)
        RealTotal = timeit.default_timer() - tick
        header = 'Points, Clock, CalcMeas, CalcTotal, RealTotal, RealMeas, MeasTime'
        CalcMeas = 2 / SMWClk
        dataOt = f'{Points},{SMWClk},{CalcMeas:.6f},{CalcMeas * Points:.6f},{RealTotal:.6f},{RealTotal / Points:.6f},{MeasTime}'
        print(f'{dataOt},{validateData(val.split(","))}')
        # validateData(val.split(','))
        time.sleep(WvSamp / SMWClk)

# FSW.write('LIST:POW:STAT OFF')                      # List Evaluation Off
# FSW.write("@LOC")
