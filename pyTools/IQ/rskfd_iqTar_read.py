from rskfd.iq_data_handling.iqdata import ReadIqTar

IQData = ReadIqTar('rskfd_iqTar_read.iq.tar')
print(f'IQ Points: {len(IQData[0])}')
print(f'SampleRat: {IQData[1]} Hz')
