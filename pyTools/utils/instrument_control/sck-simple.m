pkg load instrument-control

function rdStr = sQuery(s, SCPI)
   sWrite(s, SCPI);
   %printf("%6f",s.bytesavailable);
   rdStr = char(fread(s, 100));                 # read 100 bytes
   printf(rdStr);
end

function sWrite(s, SCPI)
   fwrite(s, strcat(SCPI,"\n"));
end

s = tcpip("192.168.58.115", 5025);
set(s,'Timeout',1);
%set(s, 'InputBufferSize', 30000);

fopen(s);
sQuery(s,"*IDN?");
sQuery(s,"SYST:ERR?");
fclose(s)
