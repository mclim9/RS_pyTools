from fesystem.instr.fe_system import FeSystem
from fesystem.instr.vsg import VSG

FES = FeSystem()
FES.vsgs = [VSG(), VSG()]
FES.ipAddrs = ['192.168.58.115', '192.168.58.115']
FES.paths = [1, 2]
FES.freq_offsets = [-3e9, 2e9, 1e9, 3e9]
FES.freqMode = 0
FES.init_sys()
FES.vsgs[0].set_fe50()
FES.set_sys_freq(45e9)  # default freqMode = 0
FES.set_sys_power(14)
FES.set_sys_rf('ON')
# FES.set_sys_power_offset(2)
# FES.set_vsg_waveform(0, '')
FES.close()
