from iSocket import iSocket                         # Import socket module

def SMW_K144_create_waveform():
    SMW.tick()
    SMW.write(':SOUR1:BB:NR5G:QCKS:GEN:DUPL TDD')       # TDD | FDD
    SMW.write(':SOUR1:BB:NR5G:QCKS:GEN:CARD FR1GT3')    # Freq Range
    SMW.write(':SOUR1:BB:NR5G:QCKS:GEN:CBW BW100')      # QS RF BW
    SMW.write(':SOUR1:BB:NR5G:QCKS:GEN:SCSP SCS30')     # QS SCS
    SMW.write(':SOUR1:BB:NR5G:QCKS:GEN:ES:RBN 273')     # QS RB
    SMW.write(':SOUR1:BB:NR5G:QCKS:GEN:ES:MOD QPSK')    # QS Modulation
    SMW.query(':SOUR1:BB:NR5G:QCKS:APPL;*OPC?')         # Apply Quick Set
    SMW.query(':SOUR1:BB:NR5G:NODE:RFPH:MODE 0')        # Phase Comp Off
    SMW.query(':SOUR1:BB:NR5G:STAT 1;*OPC?')
    SMW.tock('Quick Set to Memory')

def SMW_Get_Dir(SMW, dir='//var//user//'):
    SMW.write(f'MMEM:CDIR "{dir}"')
    readList = SMW.query(f':MMEM:CAT?').split(',')
    numfiles = SMW.queryInt(f':MMEM:CAT:LENG?')
    fileList = []
    for i in range(numfiles):
        item = readList[i * 3 + 2].replace('"', '')
        if item not in ['.', '..']:
            fileList.append(item)
    return fileList

def SMW_K144_mem2wv():
    SMW.tick()
    SMW.query(':SOUR1:BB:NR5G:WAV:CRE "/var/user/NR5G-Waveform.wv";*OPC?')
    SMW.tock('Wave --> File')

def SMW_Load_Arb(file):
    SMW.tick()
    SMW.write(f':SOUR1:BB:ARB:WAV:SEL "{file}"')
    SMW.query(':SOUR1:BB:ARB:STAT 1;*OPC?')
    SMW.tock('Wave --> Arb')

if __name__ == '__main__':
    SMW = iSocket().open('192.168.58.114', 5025)
    SMW.timeout(5)                                      # Timeout in seconds
    SMW_K144_create_waveform()
    SMW_K144_mem2wv()
    # SMW_Get_Dir('//var//user//ML_Data//')
