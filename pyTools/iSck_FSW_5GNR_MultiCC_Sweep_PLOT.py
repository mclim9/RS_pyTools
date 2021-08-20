import time
import pandas as pd
import matplotlib.pyplot as plt

f = __file__.split('_PLOT')[0] + '.txt'
print(f)
df = pd.read_csv(f, header=0, skiprows=2, sep=',')
print(f'Cols: {list(df.columns)}')                  # Col names

# ## Filter Data
df = df[df['Mode'].str.contains('SING')]            # filter data
# df = df[df['Freq'].str.contains('24000000000')]   # filter data

# ## Define Pivot Table
Yval = ['EVM1', 'EVM2', 'EVM3', 'EVM4']             # Y Values
Xval = ['Pwr']                                      # X Values
Cols = ['Freq', 'Mode']                             # Split value
aggg = 'mean'                                       # mean | sum
table = pd.pivot_table(df, values=Yval, index=Xval, columns=Cols, aggfunc=aggg)
print(f'Traces:{table.shape[1]} DataPts:{table.shape[0]}')

# ##############################################################################
# ## Plot Data
# ##############################################################################
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
