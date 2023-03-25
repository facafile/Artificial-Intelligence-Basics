import sys

class Clause:
    def __init__(self, value=[], parent1=None, parent2=None):
        self.value = value
        self.parent1 = parent1
        self.parent2 = parent2

def backtrack(begin,end,nil=None):
    lista = []
    for el in begin:
        print(' v '.join(el.value))
    for el in end:
        print(' v '.join(el.value))

    print("="*20)
    if nil != None:
        lista = backRecoursive(begin + end,nil)
        print("="*20)


def backRecoursive(checked, nil):
    if nil and nil.parent1:
        backRecoursive(checked,nil.parent1)
    if nil and nil.parent2:
        backRecoursive(checked,nil.parent2)
    if(nil.parent1 and nil.parent2):
        print(f"{' v '.join(nil.value)}  ({' v '.join(nil.parent1.value)} & {' v '.join(nil.parent2.value)})")




def factorisation(clause):
    return Clause(list(set(clause.value)),clause.parent1,clause.parent2)

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

    if len(final) == (len(c1) + len(c2)):
        return False

    return final

def find_new(base,sos,passed):
    new = []
    passed = [o.value for o in passed]
    for el in base:
        for el2 in sos:
            temp = Clause(resolve(el.value, el2.value), el, el2)
            if temp.value in passed or temp.value == False:
                continue
            passed.append(temp.value)
            new.append(removeTautology(factorisation(temp)))

    new = removeRedundant(sos, removeRedundant(base, new, False), False)
    #new = [Clause(list(t)) for t in set(tuple(element.value) for element in new)]

    return new


def refutationResolution(clauses):
    new_clauses = []
    for el in clauses:
        new_clauses.append(Clause(el))

    begining = [factorisation(removeTautology(i)) for i in new_clauses[:len(clauses)-1]]
    begining = removeRedundant(begining, begining, True)

    sos = negateEnd(factorisation(removeTautology(new_clauses[-1])))
    end = sos
    begining = removeRedundant(sos, begining, False)
    # sos = removeRedundant(begining, sos, False)

    all = begining + sos

    for i in range(len(all)):
        for j in range(i+1, len(all)):
            if len(all[i].value) == 1 and len(all[j].value) == 1 and negate(all[i].value[0]) == all[j].value[0]:
                backtrack(begining, end, Clause(["NIL"], all[i], all[j]))
                return True

    new = find_new(begining, sos,all)

    while True:
        if len(new) == 0:
            backtrack(begining, end)
            return False

        for el in new:
            if len(el.value) == 1:
                values = [o.value for o in all]
                for el2 in all:
                    if [negate(el.value[0])] == el2.value:
                        backtrack(begining, end, Clause(["NIL"], el2, el))
                        return True
        all.extend(new)

        sos = removeRedundant(sos, new, False)
        sos = removeRedundant(begining, sos, False)
        new = find_new(begining, sos, all)


def chooseRecipes(clauses, commands):
    for el in commands:
        com = el.pop(-1)

        if com == "?":
            merged = clauses + [el]
            conclusion = refutationResolution(merged)
            test = ' v '.join(el)
            message = test + " is true" if conclusion else test + " is unknown"
            print("[CONCLUSION]:", message)


        elif com == "+":
            clauses = clauses + [el]

        else:
            new_clauses = []
            for i in range(len(clauses)):
                if set(clauses[i]) != set(el):
                    new_clauses.append(clauses[i])

            clauses = new_clauses


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
        if new[i].value in to_remove:
            continue

        A = set(new[i].value)
        if len(A) == 0:
            continue

        x = (i+1) if same else 0
        for j in range(x, len(clauses)):
            if clauses[j].value in to_remove:
                continue

            B = set(clauses[j].value)

            if len(B) == 0:
                continue

            if A.issubset(B) or B.issubset(A):

                if len(A) <= len(B):
                    if same and clauses[j].value not in to_remove:
                        final.append(clauses[j])
                    to_remove.append(clauses[j].value)
                else:
                    if same and new[i].value not in to_remove:
                        final.append(new[i])
                    to_remove.append(new[i].value)


        if new[i].value not in to_remove:
            final.append(new[i])

    return final

def negate(el):
    if el.startswith("~"):
        return el[1:]

    return "~"+el

def negateEnd(end):
    clauses = []

    for el in end.value:
        clauses.append(Clause([negate(el)]))

    return clauses


def removeTautology(clause):
    atoms = set()

    for el in clause.value:
        if el in atoms:
            return Clause()

        atoms.add(negate(el))

    return clause



if __name__ == '__main__':
    sys_args = sys.argv[1:]

    c = open(sys_args[1], encoding="utf-8")

    clauses = removeComments(c)
    final_clause = clauses[-1]
    clauses = list(map(lambda str: str.lower().split(" v "), clauses))

    if len(sys_args) == 2:
        conclusion = refutationResolution(clauses)
        message = final_clause.lower()+" is true" if conclusion else final_clause.lower()+" is unknown"
        print("[CONCLUSION]:",message)



    elif len(sys_args) == 3:
        com = open(sys_args[2], encoding="utf-8")
        commands = removeComments(com)
        commands = list(map(lambda str: str.lower().replace(" v ", " ").split(" "), commands))
        conclusion2 = chooseRecipes(clauses, commands)




