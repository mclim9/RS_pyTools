from fesystem.instr.fe_system import FeSystem
from fesystem.instr.vsg import VSG
from fesystem.instr.vsa import VSA


FSW = VSA().open('192.168.58.109')
FSW.set_sweepCont('OFF')

f = open(__file__.split('.')[0] + '.log', "a")
FES = FeSystem()
FES.vsgs = [VSG(), VSG()]
FES.ipAddrs = ['192.168.58.114', '192.168.58.114']
FES.paths = [1, 2]
FES.freq_offsets = [-3e9, -2e9, 1e9, 3e9]
FES.freqMode = 0
FES.init_sys()
f.write('Frequency, SMW_IF, SMW_Band, FSW_IF, FSW_Band, FSW_Mkr_X, FSW_Mkr_Y\n')
for freq in range(110000000000, 170100000000, 100000000):
    FES.vsgs[0].set_freq(freq)
    FSW.set_freq(freq)
    FSW.set_sweepOnce()
    FSW.set_mkr_peak()
    smw_if   = FES.vsgs[0].get_if()
    smw_if_c = FES.vsgs[0].query('SOUR1:EFR:FREQ:BAND:CONF:SEL?')
    fsw_if   = FSW.get_if()
    fsw_if_c = FSW.get_if_config()
    fsw_mkrx = FSW.get_mkr_x()
    fsw_mkry = FSW.get_mkr_y()
    rdStr    = f'{freq}, {smw_if}, {smw_if_c}, {fsw_if}, {fsw_if_c}, {fsw_mkrx}, {fsw_mkry}\n'
    f.write(rdStr)
FES.close()
