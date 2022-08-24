pkg load instrument-control

v = visadev("TCPIP0::192.168.58.109::inst0::INSTR");
fopen(v)
v.Terminator = "CR";
fprintf(v,"*IDN?")
data = fscanf(v)
