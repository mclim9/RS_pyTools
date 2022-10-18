from rskfd.iq_data_handling.iqdata import WriteIqTar

IQData = [[(-1.081e-05-9.255e-05j), (0.0001+0.0001j), (-9.615e-05-9.2551e-05j), (1.0818e-05-0.0001j), (0.0002+8.6541e-05j), (-0.0001-4.0867e-05j), (-9.615e-05+2.283e-05j), (-6.731e-05-9.255e-05j), (5.288e-05+7.091e-05j), (0.0001-9.0147e-05j)]]
WriteIqTar(IQData, 3200000, 'rskfd_iqTar_write.iq.tar')
print(f'IQ Points: {len(IQData)}')
print(f'SampleRat: {IQData[1]} Hz')
