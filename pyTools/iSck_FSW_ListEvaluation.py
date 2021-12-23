""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket

def validateData(dataArry):
    for i, meas in enumerate(dataArry):
        try:
            curr = float(dataArry[i])
            nxt1 = float(dataArry[i + 1])
            delt = int(round(nxt1 - curr))
            print(f'{delt},', end='')
        except IndexError:
            pass
        except Exception as ex:
            print(f"Exception: {type(ex).__name__} Arg:\n{ex.args}")
    print('')


# #############################################################################
# ## Main Code
# #############################################################################
SMW = iSocket().open('192.168.58.114', 5025)
FSW = iSocket().open('192.168.58.109', 5025)
FSW.timeout(10)


SMW.write(':SOUR1:BB:ARB:WAV:SEL "/var/user/listmode/SquareMarker"')
SMW.write(':SOUR1:BB:ARB:CLOC 1KHz')
SMW.write(':OUTP1:TM1:SIGN MARKA1')
SMW.write(':SOUR1:BB:ARB:STATe 1')
SMW.write(':SOUR1:IQ:STATe 0')

SMW.write(':OUTP1:STAT 1')
SMW.write(':SOUR1:LIST:SEL "/var/user/listmode/listmode_pwrSweep"')
SMW.write(':SOUR1:LIST:MODE STEP')
SMW.write(':SOUR1:LIST:TRIG:SOUR EXT')
SMW.write(':SOUR1:FREQ:MODE LIST')

FSW.write(':INST:SEL "SPECTRUM"')                   # Select Analog Demod
FSW.write(':INIT:CONT OFF')                         # Cont Sweep Off
FSW.write('INIT:IMM;*OPC?')                         # Single Sweep
FSW.write("LIST:POW:SET OFF,ON,OFF,EXT,POS,0,0")    # PkPwr, RMS, Avg, TrgSource, TrgSlope,TrgOffset, GateLen

freqs = ['1GHz'] * 21                               # freqs = ["1GHz", "1GHz", "1GHz", "1GHz", "1GHz", "1GHz"]
lst = []
for freq in freqs:
    lst.append(f'{freq},0,10,OFF,NORM,1MHZ,1MHZ,1us,0')    # Freq; RefLvl; Atten; EAttn; FilterType, RBW, VBW, MeasTime, TriggerLevel
lstcmd = "LIST:POW? " + ','.join(lst)

val = FSW.query(lstcmd).split(',')
validateData(val)

FSW.write('LIST:POW:STAT OFF')                      # List Evaluation Off
# FSW.query("@LOC; *OPC?")

# tick = timeit.default_timer()
# val = FSW.query(lstcmd)
# timeDelta = timeit.default_timer() - tick
# print(f'TTime: {timeDelta:.6f} sec')
