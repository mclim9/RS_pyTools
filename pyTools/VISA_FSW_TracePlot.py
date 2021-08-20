""" Rohde & Schwarz Automation for demonstration use."""
from iVISA import iVISA
import matplotlib.pyplot as plt


# #########################################################
# ## Main Code
# #########################################################
inst = iVISA().open('192.168.58.109')

yArry = inst.query(':TRAC1:DATA? TRACE2').split(',')
xArry = inst.query(':TRAC1:DATA:X? TRACE2').split(',')
yVals = [float(ele) for ele in yArry]
xVals = [float(ele) for ele in xArry]

plt.clf()
plt.subplot(2, 1, 1)                    # Time Domain
plt.title("Trace")
plt.plot(xVals, yVals)
plt.xlabel('Freq')
plt.ylabel('magnitude')
plt.grid(True)

plt.subplot(2, 1, 2)
plt.title("BlueY YellowX")
plt.plot(yVals, "b", yVals, "b")
plt.plot(xVals, "y", xVals, "y")
# plt.xlim(-3e6,3e6)
plt.grid(True)
plt.show()
