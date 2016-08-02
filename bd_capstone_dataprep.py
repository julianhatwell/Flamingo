from pathlib import WindowsPath, PureWindowsPath
import csv

fileloc = 'C:/Dev/Study/Hadoop/big_data_capstone_datasets_and_scripts/'
folders = ('chat', 'combined', 'flamingo')

allData = dict()
for folder in folders:
    folder = folder + '-data'
    path = WindowsPath(fileloc + folder)
    if folder == 'chat-data':
        pattern = '*with_header.csv'
    else: pattern = '*.csv'
    files = sorted(path.glob(pattern))
    for file in files:
        filePath = PureWindowsPath(file)
        fname = filePath.stem
        filePath = WindowsPath(file)
        cols = dict()
        with filePath.open() as f:
            dialect = csv.Sniffer().sniff(f.read(1024))
            f.seek(0)
            dataReader = csv.reader(f, dialect)
            rownum = 0
            for row in dataReader:
                rownum = rownum + 1
                if rownum == 1:
                    colNames = row
                    for col in colNames:
                        cols[col] = []
                else:
                    for i in range(len(row)):
                        cols[colNames[i]].append(row[i])
        allData[fname] = cols
