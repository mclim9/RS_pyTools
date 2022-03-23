import numpy             as np
import matplotlib.pyplot as plt

global IData
FC1 = 1e6
OverSamp = 10
maxAmpl = 1
numPeriods = 1
IData = []
QData = []

def Gen1Tone_IQ(IData, QData):
    # ## I:Cos Q:Sin  -Frq:Nul +Frq:Pos 1.000 Normal Case

    Fs = OverSamp * FC1                         # Sampling Frequency
    StopTime = numPeriods / FC1                 # Waveforms
    t = np.linspace(0, StopTime, num=OverSamp * numPeriods, endpoint=False)     # Create time array
    IData = np.cos(2 * np.pi * FC1 * t)
    QData = np.sin(2 * np.pi * FC1 * t)

    # ## Clipping
    maxA = maxAmpl
    for i, currVal in enumerate(IData):
        if currVal > maxAmpl:
            IData[i] = maxA
        if currVal < -maxAmpl:
            IData[i] = -maxA
    for i, currVal in enumerate(QData):
        if currVal > maxAmpl:
            QData[i] = maxA
        if currVal < -maxAmpl:
            QData[i] = -maxA

    print(f"GenCW: {FC1/1e6:.3f}MHz tone RBW:{FC1 / numPeriods / 1e3:.3f}kHz")
    print(f"GenCW: {Fs/FC1:.2f} Oversample")

def plot_IQ_Time(IData, QData):
    plt.clf()
    plt.subplot(1, 1, 1)                                # (num, x, y)
    plt.title("Title")
    plt.plot(IData, "b", IData, "b")
    # plt.plot(self.QData, "y", self.QData, "y")
    plt.grid(True)
    plt.show(block=False)
    plt.pause(2)
    plt.close()

Gen1Tone_IQ(IData, QData)
plot_IQ_Time(IData, QData)
