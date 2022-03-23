fileIn = open('scpi.txt', 'r')
fileOut = open('scpi_filtered.txt', 'w')
Lines = fileIn.readlines()

for line in Lines:
    if line != '\n':
        header = line.split(' ')[0]
        if int(header) == 70:
            fileOut.write('\n')
            fileOut.write(line[62:])
        if int(header) > 70:
            fileOut.write(line[56:])


fileOut.close()
