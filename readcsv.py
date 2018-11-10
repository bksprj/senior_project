import csv

with open('uploads/test.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')

    testDict = {}
    for row in spamreader:
        # print(', '.join(row))
        # print(row)
        testDict[row[0]] = row[1]
    print(testDict)
