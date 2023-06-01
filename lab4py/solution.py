import csv
import numpy as np
import math
import argparse
import random

global header
global nn
global PRINT

class NN:
    def __init__(self,hLayers):

        self.hLayers = [len(header) - 1]
        self.hLayers += [int(x) for x in hLayers.strip("s").split("s")]
        self.hLayers += [1]

        self.W = []
        self.b = []

        self.errorVal = 0

        self.initialise_NN()

    def initialise_NN(self):
        for i in range(1,len(self.hLayers)):
            self.W.append(np.random.normal(0, 0.01, size=(self.hLayers[i - 1], self.hLayers[i])))
            self.b.append(np.random.normal(0, 0.01, size=(self.hLayers[i], 1)))


    def transition_function(self, x):
        return 1 / (1 + np.exp(-x))

    def out(self, X):
        start = X
        for i in range(len(self.W)):
            pom = np.add(np.dot(start,self.W[i]), self.b[i].T)
            if i < (len(self.W) - 1):
                pom = self.transition_function(pom)

            start = pom

        return pom

    def error(self,X,Y):
        N = len(X)
        predictions = self.out(X)

        errors = np.power(np.subtract(Y.T, predictions), 2)
        total_error = np.sum(errors)
        final = total_error / N
        self.errorVal = final

        return final

def cross(p1, p2):
        d_W =[]
        d_b =[]
        for i in range(len(p1.W)):
            d_W.append(np.multiply(np.add(p1.W[i], p2.W[i]), 0.5))
        for i in range(len(p1.b)):
            d_b.append(np.multiply(np.add(p1.b[i], p2.b[i]), 0.5))
        d = NN(nn)
        d.W = d_W
        d.b = d_b
        return d

def chooseParents(P, X, Y):
        fit = []
        sum = 0
        for el in P:
            f = 1/el.error(X, Y)
            sum += f
            fit.append(f)

        P1 = P[0]
        P2 = P[1]
        p1 = random.uniform(0.0, sum)
        pom_sum = 0
        for i in range(len(fit)):
            pom_sum += fit[i]
            if pom_sum >= p1:
                P1 = P[i]
                sum -= fit[i]
                fit[i] = 0
                break

        p2 = random.uniform(0.0, sum)
        pom_sum = 0
        for i in range(len(fit)):
            pom_sum += fit[i]
            if pom_sum >= p2:
                P2 = P[i]
                break
        return P1, P2

def elite(P, eliteNum):
        p_sorted = sorted(P, key=lambda obj: obj.errorVal)
        return p_sorted[:eliteNum]

def mutate(d, K, p):
    XX = []
    XB = []
    for el in d.W:
        xx = np.random.normal(0, K)
        matrix = np.random.choice([xx, 0], size=el.shape, p=[p, 1 - p])
        XX.append(np.add(matrix, el))

    for el in d.b:
        xx = np.random.normal(0, K)
        matrix = np.random.choice([xx, 0], size=el.shape, p=[p, 1 - p])
        XB.append(np.add(matrix, el))

    d.W = XX
    d.b = XB
    return d


def gen_alg(vel_pop, iter, elitism, p, K, X, Y, X2, Y2):
    P = np.array([NN(nn) for i in range(vel_pop)])
    for el in P:
        el.error(X, Y)
    for i in range(iter):
        new_P = elite(P, elitism)
        while len(new_P) < vel_pop:
            p1, p2 = chooseParents(P, X, Y)
            d = cross(p1, p2)
            d = mutate(d, K, p)
            new_P.append(d)
        P = new_P
        for el in P:
            el.error(X, Y)
        if ((i+1) % PRINT == 0 and i != 0):
            print("[Train error @" + str(i+1) + "]: " + str(elite(P,1)[0].errorVal))
    print("[Test error]: ", str(elite(P,1)[0].error(X2, Y2)))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', type=str)
    parser.add_argument('--test', type=str)
    parser.add_argument('--nn', type=str)
    parser.add_argument('--popsize', type=int)
    parser.add_argument('--elitism', type=int)
    parser.add_argument('--p', type=float)
    parser.add_argument('--K', type=float)
    parser.add_argument('--iter', type=int)

    args = parser.parse_args()

    nn = args.nn
    popsize = args.popsize
    elitism = args.elitism
    p = args.p
    K = args.K
    iter = args.iter
    PRINT = 2000

    rows = []
    X = []
    Y = []

    X2 = []
    Y2 = []

    with open(args.train, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)

        for row in csvreader:
            rows.append(row)

    for el in rows:
        Y.append(el[-1])
        X.append(el[:-1])

    rows2 = []
    with open(args.test, 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader)

        for row in csvreader:
            rows2.append(row)

    for el in rows2:
        Y2.append(el[-1])
        X2.append(el[:-1])

    Y = np.matrix([float(y) for y in Y])
    X = np.matrix([[float(x) for x in sublist] for sublist in X])
    Y2 = np.matrix([float(y) for y in Y2])
    X2 = np.matrix([[float(x) for x in sublist] for sublist in X2])

    gen_alg(popsize, iter, elitism, p, K, X, Y, X2, Y2)



