import sys

def factorisation(clause):
    return list(set(clause))

def resolve(c1, c2):
    setA = set(c1)
    setB = set(c2)
    final = []
    for el in setA:
        if (negate(el)) not in setB:
            final.append(el)
    for el in setB:
        if (negate(el)) not in setA:
            final.append(el)


    return final

def find_new(base,sos):
    new = []

    for el in base:
        for el2 in sos:
            temp = resolve(el, el2)

            if len(temp) < (len(el) + len(el2)):

                new.append(removeTautology(factorisation(temp)))
    print(removeRedundant(base, new, False))
    new = removeRedundant(sos, removeRedundant(base, new, False), False)
    new = [list(t) for t in set(tuple(element) for element in new)]

    return new


def refutationResolution(clauses):
    begining = [factorisation(removeTautology(i)) for i in clauses[:len(clauses)-1]]
    begining = removeRedundant(begining, begining, True)

    sos = negateEnd(factorisation(removeTautology(clauses[-1])))
    sos = removeRedundant(begining, sos, False)
    all = begining + sos
    if len(sos) == 0:
        return True

    new = find_new(begining, sos)

    while True:
        for el in new:
            for el2 in el:
                if [negate(el2)] in all:
                    return True
        all.extend(new)


        if len(new) == 0:
            return False
        if [] in new:
            return True
        sos = removeRedundant(sos, new, False)
        sos = removeRedundant(begining, sos, False)
        new = find_new(begining, sos)



def chooseRecipes():
    print("da")



def removeComments(file):
    clauses = []
    line = file.readline()

    while line:
        if not line.startswith("#"):
            clauses.append(line.strip())

        line = file.readline()

    return clauses


def removeRedundant(clauses, new, same):
    to_remove = []
    final = []

    for i in range(0,len(new)):
        if new[i] in to_remove:
            continue

        A = set(new[i])
        x = (i+1) if same else 0
        for j in range(x, len(clauses)):
            if clauses[j] in to_remove:
                continue

            B = set(clauses[j])

            if A.issubset(B) or B.issubset(A):
                if len(A) <= len(B):
                    to_remove.append(clauses[j])
                else:
                    to_remove.append(new[i])

        if new[i] not in to_remove:
            final.append(new[i])

    return final

def negate(el):
    if el.startswith("~"):
        return el[1:]

    return "~"+el

def negateEnd(end):
    clauses = []

    for el in end:
        clauses.append([negate(el)])

    return clauses


def removeTautology(clause):
    atoms = set()

    for el in clause:
        if el in atoms:
            return

        atoms.add(negate(el))

    return clause


if __name__ == '__main__':
    #sys_args = sys.argv[1:]
    c = open("resolution_ai.txt", encoding="utf-8")

    clauses = removeComments(c)
    clauses = list(map(lambda str: str.lower().split(" v "), clauses))
    #print(clauses)

    com = open("cooking_chicken_alfredo_input.txt", encoding="utf-8")
    commands = removeComments(com)
    commands = list(map(lambda str: str.lower().replace(" v "," ").split(" "), commands))
    #print(commands)

    conclusion = refutationResolution(clauses)
    print(conclusion)
    #print("[CONCLUSION]:",conclusion)

    #conclusion2 = chooseRecipes(commands)
    #print("[CONCLUSION]:", conclusion2)






