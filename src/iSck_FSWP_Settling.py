"""Rohde & Schwarz Automation for demonstration use. """
from iSocket import iSocket                               # Import socket module

# ##############################################################################
# ## Main Code
# ##############################################################################
s = iSocket().open('192.168.58.114', 5025)
s.write(':SOUR1:FREQ:CW 10e9')
s.write(':SOUR1:POWer:POW -10')
s.write(':SOUR1:FM1:STAT 1')
s.write(':SOUR1:FM1:DEV 50e6')
s.write(':SOUR1:LFO1:SHAP PULS')
s.write(':SOUR1:LFO1:SHAP:PULS:PER 0.005')
s.write(':OUTPut1:STATe 1')
s.close

# ## FSW Config
s = iSocket().open('192.168.58.109', 5025)
s.write(':SYST:DISP:UPD ON')
s.query(":INST:SEL 'Spectrum';*OPC?")
s.write(':SENS:FREQ:SPAN 43e9')
s.write(':DISP:WIND1:SUBW:TRAC1:MODE MAXH')
s.write(':INIT:CONT ON')

# ## Find center frequency
s.query(':INIT:IMM;*OPC?')
s.write(':CALC1:MARK1:STAT ON')
s.write(':CALC1:MARK1:MAX:PEAK')
s.write(':CALC1:MARK1:FUNC:CENT')
s.write(':SENS:FREQ:SPAN 500e6')

s.query(':INIT:IMM;*OPC?')
s.write(':CALC1:MARK1:MAX:PEAK')
s.write(':CALC1:MARK1:FUNC:CENT')
s.write(':INST:COUP:CENT ALL')

# ## Analog Demod Measurment
s.write(':INST:CRE:NEW ADEM, "Analog Demod"')
s.query(":INST:SEL 'Analog Demod';*OPC?")
s.write(':DISP:WIND1:SUBW:TRAC:Y:SCAL:PDIV 2e6')    # Y Range
s.write(':SENS:BWID:DEM 3e6')                       # DBW
s.write(':SENS:ADEM:MTIM 0.002')                    # Measure Time
s.write(':TRIG:SEQ:SOUR IFP')                       # IF Pwr Trigger
s.write(':TRIG:SEQ:HOLD -100e-6')                   # Trigger Offset
s.write(':CALC1:MARK1:STAT ON')

s.write(':DISP:WIND1:SUBW:TRAC:Y:SCAL:PDIV 100e3')  # Y Range
s.write(':SENS:BWID:DEM 0.4e6')                     # DBW
s.write(':SENS:ADEM:MTIM 0.5e-3')                   # Measure Time
s.write(':SENS:FILT1:LPAS:FREQ:REL 10')             # Low Pass Filter Setting  MMM
s.write(':SENS:FILT1:LPAS:STAT ON')                 # Low Pass Filter ON
