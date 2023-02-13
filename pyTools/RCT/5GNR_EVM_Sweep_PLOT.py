import time
import pandas as pd
import matplotlib.pyplot as plt


f = __file__.split('_PLOT')[0] + '.csv'
# f = '5GNR_EVM_Sweep_PVT_SMW.csv'
print(f)
df = pd.read_csv(f, header=0, skiprows=0, sep=',')
print(f'Cols: {list(df.columns)}')                  # Col names

# ## Filter Data
df = df[df['Instrument'].str.contains('PVT_2_PVT')]           # filter data

# ## Define Pivot Table
Yval = ['EVM_dB']                                   # Y Values
Xval = ['Pwr']                                      # X Values
Cols = ['Instrument', 'Freq', 'Wave']               # Split value
aggg = 'mean'                                       # mean | sum
table = pd.pivot_table(df, values=Yval, index=Xval, columns=Cols, aggfunc=aggg)
print(f'Traces:{table.shape[1]} DataPts:{table.shape[0]}')

table.plot(legend=True)
# plt.figure(figsize=(5, 5), dpi=200)
# plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0.0), ncol=2)
plt.legend(bbox_to_anchor=(0.3, 1.1))
# plt.tight_layout(pad=2)
plt.grid()
plt.title(f'{Yval} {aggg}')
plt.axis([-50, 10, -55, -30])                     # X, Y
plt.grid(b=True, which='minor', color='c', linestyle='--')
plt.grid(b=True, which='major', color='b')
plt.minorticks_on()
plt.xlabel(Xval)
plt.ylabel(Yval)

plt.savefig(f'{f}.png')
plt.show()
time.sleep(1)
plt.close()
