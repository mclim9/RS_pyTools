import time
import pandas as pd
import matplotlib.pyplot as plt


f = 'rtp-cable-calibration.csv'

print(f)
df = pd.read_csv(f, header=0, skiprows=0, sep=',')
print(f'Cols: {list(df.columns)}')                  # Col names

# ## Filter Data
# df = df[df['Mode'].str.contains('EVM')]           # filter data

# ## Define Pivot Table
Yval = ['Channel_2 Delay (ps)', 'Channel_3 Delay (ps)', 'Channel_4 Delay (ps)']                      # Y Values
Xval = ['SMW Frequency (GHz)']                      # X Values
# Cols = ['Freq', 'Mode', 'Gen']                    # Split value
Cols = []                                           # Split value
aggg = 'mean'                                       # mean | sum
table = pd.pivot_table(df, values=Yval, index=Xval, columns=Cols, aggfunc=aggg)
print(f'Traces:{table.shape[1]} DataPts:{table.shape[0]}')

# plt.subplot(2, 1, 1)         #Time Domain
# plt.subplot(2, 1, 2)         #Time Domain
table.plot(legend=True)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2)
plt.tight_layout(pad=2)
plt.grid()
plt.title(f'{Yval} {aggg}')
# plt.axis([-50, 10, -60, -20])                     # X, Y
plt.xlabel(Xval)
plt.ylabel(Yval)

plt.savefig(f'{f}.png')
plt.show()
time.sleep(1)
plt.close()
