""" Rohde & Schwarz Automation for demonstration use."""
from iSocket import iSocket                             # Import socket module

FSW = iSocket().open('192.168.58.109', 5025)
SMW = iSocket().open('192.168.58.114', 5025)
FSW.timeout(30)                                         # Timeout in seconds

def VSG_Setup():
    SMW.write(f':SOUR1:FREQ:CW {freq}')                 # Center Frequency
    SMW.write(f':SOUR1:POW:POW {powr}')                 # RMS Power
    SMW.write(f':SOUR1:BB:WLNN:BW {SMW_bw}')            # BW
    SMW.write(f':SOUR1:BB:WLNN:FBL1:TMOD {PPDU}')       # Tx Mode
    SMW.write(f':SOUR1:BB:WLNN:FBL:USER1:MCS MCS13')    # MCS
    SMW.write(f':SOUR1:BB:WLNN:FBL:USER1:MPDU1:COUN 3') # Number of MPDU
    for i in range(MPDU):
        SMW.write(f':SOUR1:BB:WLNN:FBL:USER1:MPDU{i+1}:DATA:LENG 16000')
    SMW.write(f':SOUR1:BB:WLNN:STAT 1')                 # WLANN On
    SMW.write(f':SOUR1:CORR:OPT:EVM 1')                 # Optimize EVM
    SMW.write(f':OUTP1:STAT 1')                         # Output on

def VSA_Setup():
    FSW.write(f'*RST')
    FSW.write(f'*CLS')
    FSW.write(f':SYST:DISP:UPD ON')                     # Display ON
    FSW.write(f':INST:CRE:NEW WLAN, "WLAN"')            # WLAN channel
    FSW.write(f':INIT:CONT OFF')                        # Single Sweep
    FSW.write(f':CONF:BURS:IQ:IMM')                     # Mod; Accuracy; Flatness Meaurement
    FSW.write(f':SENS:FREQ:CENT {freq}')                # Center Frequency
    FSW.write(f':CONF:STAN {FStd}')                     # 6:n 8:ac 10ax11:be
    FSW.write(f':SENS:SWE:TIME 0.002')                  # Sweep Time
    FSW.write(f':SENS:DEM:CEST 0')
    FSW.write(f':SENS:DEM:CEST:RANG PRE2T')             # Ch Est L-LHF & EHT-LTF
    FSW.write(f':SENS:DEM:CEST:RANG PRE1T')             # Ch Est EHT-LTF
    FSW.write(f':SENS:DEM:FORM:BCON:AUTO 1')            # PPDU Same as first PPDU
    FSW.query(f':INIT:IMM;*OPC?')

def VSA_Meas_EVM():
    FSW.write(f':INST:SEL "WLAN"')                      # WLAN Channel
    FSW.write(f':CONF:BURS:IQ:IMM')                     # Mod; Accuracy; Flatness Meaurement
    print(f'EVM All  Avg: {FSW.query(f":FETC:BURS:EVM:ALL:AVER?")}')
    print(f'EVM Data Avg: {FSW.query(f":FETC:BURS:EVM:DATA:AVER?")}')

def VSA_Meas_SEM():
    FSW.write(f':INST:SEL "WLAN"')                      # WLAN Channel
    FSW.write(f':CONF:BURS:SPEC:MASK:IMM')              # SEM Meaurement

def VSA_Meas_PSD():
    FSW.write(f':INST:SEL "Spectrum"')                  # Spectrum Channel
    FSW.write(f':SENS:FREQ:CENT {freq}')                # Frequency
    FSW.write(f':SENS:FREQ:SPAN 200e6')                 # Span
    FSW.write(f':SENS:WIND1:DET1:FUNC RMS')             # Detector
    FSW.write(f':DISP:WIND1:SUBW:TRAC1:MODE MAXH')      # Trace:WRIT AVER MAXH MINH VIEW BLAN
    FSW.write(f':CALC1:MARK1:STAT ON')                  # Marker1 ON
    FSW.write(f':CALC1:MARK1:FUNC:NOIS:STAT ON')        # Marker1 Noise Marker on
    FSW.write(f':CALC1:MARK1:X {freq}')                 # Marker1 Frequency
    print(f'Noise Marker: {FSW.query(f":CALC1:MARK1:FUNC:NOIS:RES?")}')

# | Standard | Modu | Mode | PPDU | FSW |
# | -------- | ---- | ---- | ---- | --- |
# | 802.11a  | OFDM | Legy |      | 0   |
# | 802.11b  | DSSS | Legy | CCK  | 1   |
# | 802.11g  | both | Legy | L    | 4   |
# | 802.11n  | OFDM | GrnF | HT   | 6   |
# | 802.11ac | OFDM | MixM | VHT  | 8   |
# | 802.11ax | OFDM | MixM | HE   | 10  |
# | 802.11be | OFDM | MixM | EHT  | 11  |
# | 802.11bn | OFDM | TBD  | UHR  | 12  |
if __name__ == "__main__":
    rfbw    = 20
    freq    = 2.4e9
    powr    = -10
    FStd    = 6                     # 6:n 8:ac 10ax11:be
    SMW_bw  = f'BW{rfbw}'
    PPDU    = f'HT{rfbw}'
    MPDU    = 3
    VSG_Setup()
    VSA_Setup()
    # VSA_Meas_EVM()
    # VSA_Meas_SEM()
    VSA_Meas_PSD()
