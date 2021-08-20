from iSocket import iSocket                 # Import socket module
import time
smw = iSocket().open('192.168.58.114', 5025)
smw.s.settimeout(6)


channelList = [2071667, 2077917, 2084165, 2065815, 2079165, 2095833]
cellIdList = [1, 2, 3, 4]

channelList = [2079165]
cellIdList = [1]

for channel in channelList:
    for cellId in cellIdList:
        smw.query('*RST;*CLS;*OPC?')
        smw.write('SOUR:BB:NR5G:LINK UP')
        smw.write('BB:NR5G:NODE:CELL0:CARD FR2')
        smw.write('SOUR:BB:NR5G:NODE:CELL0:CARD GT6')
        smw.write(f'SOUR:BB:NR5G:NODE:CELL0:CELL {cellId}')
        smw.write('SOUR:BB:NR5G:NODE:CELL0:TXBW:S120K:USE 1')
        smw.write('SOUR:BB:NR5G:NODE:CELL0:TXBW:S60K:USE 0')
        smw.write('SOUR:BB:NR5G:UBWP:USER0:USCH:CCOD:STAT 0')
        smw.write('SOUR:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:RBN 66')
        smw.write('SOUR:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:RBOF 0')
        smw.write('SOUR:BB:NR5G:UBWP:USER0:USCH:CCOD:STAT 1')
        smw.write('SOUR:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:FRC:STATe 1')
        smw.write('SOUR:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:FRC:TYPE FR2A13')

        #  channel to frequency calculation
        freq = 24250.08 + 0.06 * (channel - 2016667)

        smw.write('SOUR:BB:NR5G:NODE:CELL0:CARD FR2')
        # smw.write(f"SOUR:FREQ:CW {freq}e+06")
        # smw.write(f"BB:NR5G:NODE:CELL0:PCFR {freq}e+06")  # MMM
        smw.write(f"SOUR:FREQ:CW {freq}e+06")
        smw.write('SOURce1:POWer:LEVel:IMMediate:AMPLitude -30')
        smw.write('SOUR:BB:NR5G:STAT 1')

        time.sleep(6)

        filename = f"FR2_UL_100M_G_FR2_A1_3_CID{cellId}_CHAN{channel}_FRC.wv"
        smw.write(f'SOUR:BB:NR5G:WAV:CRE "/var/user/{filename}"')
        smw.write(f':SOUR1:BB:NR5G:SETT:STOR "/var/user/{filename}"')
        time.sleep(1)
        while smw.query('BB:PROG:MCOD?') != '100':
            time.sleep(1)

        time.sleep(1)
        smw.query('*OPC?')

        print(smw.query('SYST:ERR:ALL?'))
        smw.write('OUTP1:STAT 1')
