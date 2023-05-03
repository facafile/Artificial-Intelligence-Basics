import math
import csv
import sys

global header


def confMatrix(guess, dataset):
    Y = sorted(list(set(dataset + guess)))
    matrix = []
    correct = 0
    for i in range(len(Y)):
        row = []
        for j in range(len(Y)):
            row.append(0)
        matrix.append(row)

    for i in range(len(dataset)):
        matrix[Y.index(dataset[i])][Y.index(guess[i])] += 1

    for i in range(len(Y)):
        correct += matrix[i][i]

    return matrix, round(correct / len(dataset),4)


def test(dataset, value):
    for el in dataset:
        if el[-1] != value:
            return False
    return True

def DFS(root, path=[]):
    path.append(root[0])
    if type(root[1]) == Leaf:
        i = 0
        out = ""
        for el in path:
            if el != None:
                i += 1
                out += str(i) + ":" + el[0] + "=" + el[1] + " "

        out += root[1].cls
        print(out)
    else:
        for el in root[1].subtrees:
            DFS(el, path)
    path.pop()

def filterDataset(dataset, index, value):
    return list(filter(lambda x: x[index] == value, dataset))

def argmax(dataset, index):
    dict = {}
    for el in dataset:
        if el[index] in dict:
            dict[el[index]] += 1
        else:
            dict[el[index]] = 1
    dict = sorted(dict.items(), key=lambda x: (-x[1],x[0]))
    return dict[0][0]

class Node:
    def __init__(self, feature, subtrees):
        self.feature = feature
        self.subtrees = subtrees

class Leaf:
    def __init__(self, cls):
        self.cls = cls

def informationalGain(dataset, feature):
    sum = 0
    index = header.index(feature)
    k = set()

    for el in dataset:
        k.add(el[index])

    for i in range(len(k)):
        setEl = k.pop()
        d2 = filterDataset(dataset, index, setEl)
        sum += round((len(d2) * entropy(d2)) / len(dataset),4)

    return round(entropy(dataset) - sum,4), feature

def entropy(dataset):
    k = set()
    sum = 0
    for el in dataset:
        k.add(el[-1])

    for i in range(len(k)):
        setEl = k.pop()
        sum += (-1) * probabilityOfY(dataset, setEl) * math.log2(probabilityOfY(dataset, setEl))

    return round(sum,4)

def probabilityOfY(dataset,y):
    probability = 0

    for el in dataset:
        if el[-1] == y:
            probability += 1

    return probability / len(dataset)
class ID3:
    def __init__(self):
        pass

    def fit(self, DS, parentDS, features, y):
        if len(DS) == 0:
            v = argmax(parentDS, -1)
            return Leaf(v)
        v = argmax(DS, -1)
        #print(DS, filterDataset(DS, len(header) - 1, v))
        #print(features)
        if features == [] or test(DS,v):
            return Leaf(v)
        #print(sorted(map(lambda x: informationalGain(DS, x), features),key=lambda x: (-x[0], x[1])))
        x = sorted(map(lambda y: informationalGain(DS, y), features),key=lambda z: (-z[0], z[1]))[0][1]
        subtrees = []

        k = set()
        index = header.index(x)
        for el in DS:
            k.add(el[index])
        s = features
        s.remove(x)
        for v in sorted(list(k)):
            t = self.fit(filterDataset(DS, index, v), DS, s, y)
            subtrees.append(((x,v), t))
        features.append(x)
        return Node(x, subtrees)

    def predict(self, dataset, tree, train):
        predicitions = []
        for el in dataset:
            helpTree = tree
            filters = []
            while True:
                index = header.index(helpTree[0][0][0])
                unrecognised = True
                for branch in helpTree:
                    if branch[0][1] == el[index]:
                        helpTree = branch[1]
                        unrecognised = False
                        break
                if type(helpTree) == Leaf:
                    predicitions.append(helpTree.cls)
                    break
                if unrecognised:
                    for filter in filters:
                        train = filterDataset(train, filter[0], filters[1])
                    predicitions.append(argmax(train, -1))
                    break

                helpTree = helpTree.subtrees
                filters.append((index, el[index]))

        return predicitions


if __name__ == '__main__':
    header = []
    rows = []
    args = sys.argv[1:]

    with open("volleyball.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)

        for row in csvreader:
            rows.append(row)

    testRows = []

    with open("data.csv", 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader)

        for row in csvreader:
            testRows.append(row)

    a = ID3()
    tree = a.fit(rows,rows,header[:-1],"")
    print("[BRANCHES]:")
    DFS((None,tree),[])

    predicitions =a.predict(testRows, tree.subtrees, rows)
    print(predicitions)
    print("[PREDICTIONS]: " + " ".join(predicitions))

    matrix, accuracy = confMatrix(predicitions,list(map(lambda x: x[-1],testRows)))
    print("[ACCURACY]: " + str(accuracy))
    print("[CONFUSION_MATRIX]:")
    for el in matrix:
        el = map(str,el)
        print(" ".join(el))

