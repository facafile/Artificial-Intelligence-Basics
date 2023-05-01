import math
import csv

def ID3():
    return


def informationalGain():
    return


if __name__ == '__main__':
    header = []
    rows = []

    with open("data.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)

        for row in csvreader:
            rows.append(row)
