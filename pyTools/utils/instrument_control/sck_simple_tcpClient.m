s = tcpclient("192.168.58.115", 5025)
s.configureTerminator("LF")             % LF = \n = 0x0A
write(s,"*IDN?")
pause(1)
%s.NumBytesAvailable
%data = read(s,100,"string")
data = read(s,1000,"string")
