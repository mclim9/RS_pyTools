""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                 # Import socket module

SMW = iSocket().open('172.24.225.120', 5025)

# def Set_IQ_Data(self):
#     IData = [0.1,0.2,0.3]
#     QData = [0.4,0.5,0.6]

#     ### ASCII
#     scpi  = ':MMEM:DATA:UNPR "NVWFM://var//user//wave.wv",#'        # Ascii Cmd
#     iqsize= str(len(IData)*4)                                       # Calculate bytes of IQ data
#     scpi  = scpi + str(len(iqsize)) + iqsize                        # Calculate length of iqsize string
#     ### Binary
#     iqdata= np.vstack((IData,QData)).reshape((-1,),order='F')       # Combine I&Q Data
#     bits  = np.array(iqdata*32767, dtype='>i2')                     # Convert to big-endian 2byte int
#     ### ASCII + Binary
#     cmd   = bytes(scpi, 'utf-8') + bits.tostring()                  # Add ASCII + Bin
#     self.K2.write_raw(cmd)
#     self.write('SOUR1:BB:ARB:WAV:CLOC "/var/user/wave.wv",1.1E6')    # Set Fs/Clk Rate
#     self.write('BB:ARB:WAV:SEL "/var/user/wave.wv"')                 # Select Arb File

def main():
    filename = 'AmpToolsDirDpd_Iter1.wv'
    filename = 'ArbMccwOutpDummy.wv'
    SMW.write(f':SOUR1:FREQ:CW 3e9')            # Center Frequency
    SMW.query(f':SOUR1:POW:LEV -10;*OPC?')      # RMS Power Level
    SMW.write(f':SOUR1:IQ:STAT 0')              # IQ Modulation OFF

    # SMW.write(f':MMEM:DATA "/var/user/')
    SMW.query(f':SOUR1:BB:ARB:WAV:SEL "/var/user/{filename}"; *OPC?')
    SMW.query(f':SOUR1:BB:ARB:STAT ON; *OPC?')
    SMW.write(f':OUTP1:STAT 0')                 # RF Output
    # SMW.write(f':SOUR1:BB:ARB:TRIG:SOUR AUTO')
    # SMW.write(f':SOUR1:BB:ARB:TRIG:OUTP1:MODE REST')
    for i in range(3):
        errStr = SMW.query(f'SYST:ERR?')
        print(errStr)

if __name__ == "__main__":
    main()
