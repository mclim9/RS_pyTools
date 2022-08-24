
s = tcpip("192.168.58.109", 5025, "Timeout", 10);
s.Terminator = 'CR';
fopen(s)
writeline(s, "*IDN?");
printf(char(readline(s)));                   % attempt to read 100 bytes

chunk = 1000;
## write(s, "FORM:DATA REAL,32")               % 4 bytes per I or Q
## write(s, "TRAC:IQ:DATA:FORM IQP")           % IQ Pairs
## recLent = int(sQuery(f':TRAC:IQ:RLEN?").decode())
## for i in range(recLent  chunk):
##     rdChunk  = sQuery(f'TRAC:IQ:DATA:MEM? {i * chunk},{chunk}")
##     rdChunk  = sQuery(f'TRAC:IQ:DATA:MEM? {i * chunk},{chunk}")
##     if len(rdChunk) < chunk * 8:
##         rdChunk  = sQuery(f'TRAC:IQ:DATA:MEM? {i * chunk},{chunk}")
##         rdChunk  = sQuery(f'TRAC:IQ:DATA:MEM? {i * chunk},{chunk}")
##         print(f'reread chunk{i}")
##     numBytes = int(chr(rdChunk[1]))         % Number of Bytes
##     numIQ    = int(rdChunk[2:2 + numBytes])
##     IQBytes  += rdChunk[(numBytes + 2):-1]  % Remove Header
##
## IQAscii  = struct.unpack("<" + 'f' * int(len(IQBytes) / 4), IQBytes)
## IQPoints = len(IQBytes) / 8                 % 4 bytes I + 4 bytes Q
## print(f'{IQPoints} IQ Points")
