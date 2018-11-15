import csv

with open('uploads/data_test.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')

    testDict = {}
    for row in spamreader:
        print(row)
        testDict[row[0]] = row[1:]
    print(testDict)
    for key,value in testDict.items():
        print(key,value)
