pkg load instrument-control

s = tcpip("192.168.58.109", 5025, "Timeout", 2);
fopen(s)
write(s, "*IDN?\n");
val = char(read(s, 100));                 # attempt to read 100 bytes
printf(val);
