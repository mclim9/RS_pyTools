from iSocket import iSocket

SMW = iSocket().open('192.168.58.114', 5025)
FSW = iSocket().open('192.168.58.109', 5025)
freqStart =  7000000000
freqStop  = 44000000000
freqStep  =   500000000

# f = open('NoiseSweep.csv', 'a')
FSW.write('INIT:CONT OFF')

print('Freq-GHz,RMS ,Noise,FSWFreq,MeasTim,Fs-MHz ,Mkr-dBm')
for freqFSW in [24, 27, 30, 37, 40, 43]:
    FSW.write(f':SENS:FREQ:CENT {freqFSW}GHz')
    for freq in range(freqStart, freqStop, freqStep):
        SMW.query(f':SOUR1:FREQ:CW {freq};*OPC?')
        ampli = SMW.queryFloat(f':SOUR1:POW:POW?')
        noiBW = SMW.queryFloat(f':SOUR1:AWGN:BWID?')
        FSW.query('INIT:IMM;*OPC?')
        FSW.write('CALC1:MARK1:MAX:PEAK')
        markY = FSW.queryFloat(':CALC1:MARK1:Y?')
        sampRat = FSW.queryFloat(':TRAC:IQ:SRAT?')
        measTim = FSW.queryFloat(':SENS:SWE:TIME?')
        outStr = f'{freq/1e9:6.3f},{ampli:6.2f},{noiBW/1e6:6.1f},{freqFSW:6.3f},{measTim:6.3f},{sampRat/1e6:6.3f},{markY:6.3f}'
        print(outStr)
        # f.write(outStr + "\n")
    # f.close()
