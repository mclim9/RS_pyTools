filename = __file__.split('.')[0] + '.csv'

def file_erase():
    fily = open(filename, '+w')
    fily.close()

def file_read():
    fily = open(filename, '+r')
    data = fily.readlines()
    fily.close()
    return data

def file_readCSV():
    data = file_read()
    outList = []
    for lin in data:
        outList.append(lin.strip().split(','))
    return outList

def file_readCSV_key(col, key):
    dataList = file_readCSV()
    outRow = "Not Found"
    for row in dataList:
        if row[col] == key:
            outRow = row
            break
    print(outRow)
    return outRow

def file_write(outString):
    fily = open(filename, '+a')
    fily.write(f'{outString}\n')
    fily.close()

if __name__ == "__main__":
    file_erase()
    for i in range(10):
        file_write(f'{i},{2 * i},{3 * i + 1}')
    file_readCSV_key(0, '6')
