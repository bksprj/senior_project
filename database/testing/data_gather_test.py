import csv

with open('data_test.csv', newline='') as csvfile:
    textreader = csv.reader(csvfile, delimiter=',')
    data_dict = {}
    for row in textreader:
            print(row, type(row))
            data_dict[row[0]] = row[1:]
    print(data_dict)
