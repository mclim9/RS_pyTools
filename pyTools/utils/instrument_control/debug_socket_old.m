s = tcpclient("192.168.58.115", 5025);
fopen(s);
fprintf(s, '*IDN?');
data = fscanf(s);
fprintf(data);
fclose(s)