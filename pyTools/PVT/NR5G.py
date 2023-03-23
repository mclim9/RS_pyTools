""" Rohde & Schwarz RTP Amplitude Measurement"""
from iSocket import iSocket

class PVT(iSocket):
    def __init__(self):
        super().__init__()

    def init_nr(self):
        self.write(f'INIT:NRS:MEA:MEV')

    def get_nr_initImm(self):
        self.query(f'FETC:NRS:MEAS:STAT?')

    def set_nr_initImm(self):
        self.write('INIT:NRS:MEAS')                         # RUN state

    def get_nr_attn(self):
        '''External Attenuation, dB'''
        return self.query(f'CONF:NRS:MEAS:RFS:EATT?')

    def set_nr_attn(self, attn):
        '''External Attenuation, dB'''
        self.write(f'CONF:NRS:MEAS:RFS:EATT {attn}')

    def get_nr_freq(self):
        '''CC Frequency, Hz'''
        return self.query(f'CONF:NRS:MEAS1:CC1:FREQ?')

    def set_nr_freq(self, freq):
        '''CC Frequency, Hz'''
        self.write(f'CONF:NRS:MEAS1:CC1:FREQ {freq}')

    def get_nr_ENP(self):
        '''Expected Nominal Power, RMS dBm'''
        return self.query(f'CONF:NRS:MEAS:RFS:ENP?')

    def set_nr_ENP(self, ENP):
        '''Expected Nominal Power, RMS dBm'''
        self.write(f'CONF:NRS:MEAS:RFS:ENP {ENP}')

    def set_nr_measInit(self):
        '''Init Measurements'''
        self.write(f'CONF:NRS:MEAS:MEV:RES:MOD ON')         # Modulation
        self.write(f'CONF:NRS:MEAS:MEV:RES:SEM OFF')        # Spectral Mask
        self.write(f'CONF:NRS:MEAS:MEV:RES:ACLR OFF')       # ACLR
        self.write(f'CONF:NRS:MEAS:MEV:RES:PMON OFF')       # Power Monitor
        self.write(f'CONF:NRS:MEAS:MEV:RES:TXP OFF')        # Tx Power
        self.write(f'CONF:NRS:MEAS:MEV:RES:PDYN OFF')       # Power Deynamics

    def get_nr_Path_VSA(self):
        '''Analyzer Path'''
        return self.query(f'ROUT:NRS:MEAS:SPAT?')

    def set_nr_Path_VSA(self, path):
        '''Analyzer Path: RF1.1; RF2.1'''
        self.write(f'ROUT:NRS:MEAS:SPAT "{path}"')

    def get_nr_phaseComp(self):
        '''Phase Compensation'''
        return self.query(f'CONF:NRS:MEAS:MEV:PCOM?')

    def set_nr_phaseComp(self, mode):
        '''Phase Compensation: OFF | CAF | UDEF'''
        self.write(f'CONF:NRS:MEAS:MEV:PCOM {mode}, 0')

    def get_nr_PUSCH(self):
        '''PUSCH DMRS Info'''
        return self.query(f'CONF:NRS:MEAS:CC1:ALL1:PUSC?')

    def set_nr_PUSCH(self, mode):
        '''PUSCH DMRS Info: Type; '''
        self.write(f'CONF:NRS:MEAS:CC1:ALL1:PUSC {mode}, 0')

    def get_nr_trigger(self):
        '''Trigger Source'''
        return self.query(f'TRIG:NRS:MEAS:MEV:SOUR?')

    def set_nr_trigger(self, mode):
        '''Trigger Source: "Free Run (No Sync)","Free Run (Fast Sync)","IF Power","Base1: Cont. 10ms Trigger","Base1: User Trigger","Base1: External TRIG A","Base1: External TRIG B" '''
        self.write(f'TRIG:NRS:MEAS:MEV:SOUR "{mode}"')

    def get_nr_UserMar(self):
        '''User Margin, Crest Factor dB'''
        return self.query(f'CONF:NRS:MEAS:RFS:UMAR?')

    def set_nr_UserMar(self, UserMar):
        '''User Margin, Crest Factor dB'''
        self.write(f'CONF:NRS:MEAS:RFS:UMAR {UserMar}')

    def file_write(outString):
        filename = __file__.split('.')[0] + '.csv'
        fily = open(filename, '+a')
        fily.write(f'{outString}\n')
        fily.close()

if __name__ == "__main__":
    pvt = PVT().open('192.168.58.30', 5025)
    pvt.s.settimeout(5)
    pvt.get_nr_PUSCH()
