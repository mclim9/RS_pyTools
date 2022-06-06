from fesystem.instr.fe_system import FeSystem
from fesystem.instr.vsg import VSG

FES = FeSystem()
FES.vsgs = [VSG(), VSG()]
FES.ipAddrs = ['192.168.58.114', '192.168.58.114']
FES.paths = [1, 2]
FES.freq_offsets = [-3e9, -2e9, 1e9, 3e9]
FES.freqMode = 0
FES.init_sys()
FES.vsgs[0].set_fe50()
FES.set_sys_freq(140e9)         # Set System center Freq
FES.set_sys_power(-10)
FES.set_sys_rf('ON')
FES.close()
