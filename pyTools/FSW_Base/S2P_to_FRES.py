import pandas as pd
from math import log, sqrt, atan2

def file_write(filename, outString):
    fily = open(filename, '+a')
    fily.write(f'{outString}\n')
    fily.close()

def s2p_to_fres_RI(fily):
    filename = fily.split('.')[0] + '.fres'
    df = pd.read_csv(fily, header=0, skiprows=4, sep=' ')
    print(df.columns)

    fily = open(filename, 'w')
    file_write(filename, '#  HZ   S   RI   R     50.00')
    file_write(filename, '! Measurements: S21')
    file_write(filename, '!')
    for i, freq in enumerate(df['!freq']):
        file_write(filename, f'{freq}  {df.ReS21[i]:9.6f}  {df.ImS21[i]:9.6f}')

def s2p_to_fres_DB(fily):
    filename = fily.split('.')[0] + '.fres'
    df = pd.read_csv(fily, header=0, skiprows=4, sep=' ')
    print(df.columns)

    fily = open(filename, 'w')
    file_write(filename, '#  HZ   S   DB   R     50.00')
    file_write(filename, '! Measurements: S21')
    file_write(filename, '!')
    for i, freq in enumerate(df['!freq']):
        mag   = sqrt(df.ReS21[i] * df.ReS21[i] + df.ImS21[i] * df.ImS21[i])
        dB    = -10 * log(mag)
        phase = atan2(df.ImS21[i], df.ReS21[i])
        file_write(filename, f'{freq}  {dB:9.6f}  {phase:9.6f}')

if __name__ == "__main__":
    s2p_to_fres_RI('S2P_to_FRES.s2p')
