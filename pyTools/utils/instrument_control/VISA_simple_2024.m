% pkg load instrument-control

% resourcelist = visadevlist
v = visadev('TCPIP0::172.24.225.100::inst0::INSTR');
configureTerminator(v,"CR/LF");
writeline(v,"*IDN?");
data = readline(v);
