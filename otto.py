import os


def loadData(filename):
    "Load data from the CSV training and test files"
    data = []
    fin = open(filename, 'r')
    line = fin.readline()
    while (line != ''):
        data.append(line.strip('\n'))
        line = fin.readline()
    fin.close()
    return data[1:]

data = loadData("test.csv")
print data[:2]
