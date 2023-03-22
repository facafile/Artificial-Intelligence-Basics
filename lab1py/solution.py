import heapq
import sys


class Node:
    def __init__(self, st=None, value=None, parent=None, summed=None):
        self.st = st
        self.value = value
        self.parent = parent
        self.summed = summed

    def __lt__(self, other):
        return (self.summed, self.st) < (other.summed, other.st)

    def __eq__(self, other):
        if (other == None):
            return False
        if (not isinstance(other, Node)):
            return False
        return self.summed == other.summed and self.st == other.st


def isOptimisticH(transfers, weight, end_states):
    prt_str = ""
    conclusion1 = "Heuristic is optimistic."
    conclusion2 = "Heuristic is not optimistic."
    test_case = True
    for key in sorted(weight.keys()):
        solution_found, closed, ln, value, path = UCS(key, end_states, transfers)
        state = "[CONDITION]: " + ("[OK]" if float(value) >= weight[key] else "[ERR]")
        prt_str += state + " h(" + key + ") <= h*: " + str(weight[key]) + " <= " + value + "\n"
        if (not float(value) >= float(weight[key])):
            test_case = False

    prt_str += "[CONCLUSION]: " + (conclusion1 if test_case else conclusion2)
    return prt_str


def isConsistentH(transfers, weight):
    prt_str = ""
    conclusion1 = "Heuristic is consistent."
    conclusion2 = "Heuristic is not consistent."
    test_case = True

    for key in sorted(transfers.keys()):
        for el in sorted(transfers[key]):
            if len(el) == 2:
                state = "[CONDITION]: " + ("[OK]" if weight[el[0]] + float(el[1]) >= weight[key] else "[ERR]")
                prt_str += state + " h(" + key + ") <= h(" + el[0] + ") + c: " + str(weight[key]) + " <= " + str(
                    weight[el[0]]) + " + " + str(float(el[1])) + "\n"
                if not weight[el[0]] + float(el[1]) >= weight[key]:
                    test_case = False

    prt_str += "[CONCLUSION]: " + (conclusion1 if test_case else conclusion2)
    return prt_str


def A_STAR(first, last, transfers, weight):
    open = []
    heapq.heappush(open, Node(first, 0, None, weight[first]))
    closed = set()
    solution_found = False
    path = []
    value = 0
    ln = 0

    while open:
        v = heapq.heappop(open)
        if v.st in last:
            closed.add(v.st)
            value, path, ln = backtrack(v)
            solution_found = True
            break

        list = transfers[v.st]
        if v.st not in closed:
            for i in range(len(list)):
                if list[i][0] not in closed:
                    heapq.heappush(open, Node(list[i][0], float(list[i][1]), v,
                                              float(list[i][1]) + float(v.summed) - float(weight[v.st]) + float(
                                                  weight[list[i][0]])))
            closed.add(v.st)

    return solution_found, closed, ln, value, path


def backtrack(node):
    value = 0.
    ls = ""
    ln = 0
    while node.parent:
        ln += 1
        value += float(node.value)
        ls = " => " + str(node.st) + ls
        node = node.parent
    ls = node.st + ls
    ln += 1
    return (str(value), ls, ln)


def BFS(first, last, transfers):
    open = [Node(first, 0, None, None)]
    closed = set()
    solution_found = False
    path = []
    value = 0
    ln = 0

    while open:
        v = open.pop(0)
        if v.st in last:
            closed.add(v.st)
            value, path, ln = backtrack(v)
            solution_found = True
            break

        list = transfers[v.st]
        list_sorted = sorted(list, key=lambda x: (x[0]))
        if v.st not in closed:
            for i in range(len(list)):
                if list_sorted[i][0] not in closed:
                    open.append(Node(list_sorted[i][0], list_sorted[i][1], v, None))
            closed.add(v.st)

    return solution_found, closed, ln, value, path


def UCS(first, last, transfers):
    open = []
    heapq.heappush(open, Node(first, 0, None, 0))
    closed = set()
    solution_found = False
    path = []
    value = 0
    ln = 0

    while open:
        v = heapq.heappop(open)
        if v.st in last:
            closed.add(v.st)
            value, path, ln = backtrack(v)
            solution_found = True
            break

        list = transfers[v.st]
        if v.st not in closed:
            for i in range(len(list)):
                if list[i][0] not in closed:
                    heapq.heappush(open, Node(list[i][0], float(list[i][1]), v, float(list[i][1]) + float(v.summed)))
            closed.add(v.st)

    return solution_found, closed, ln, value, path


if __name__ == '__main__':
    arg_list = sys.argv[1:]
    i = 0
    my_alg = ""
    s_path = ""
    h_path = ""
    doOpt = False
    doCons = False
    include_h = False
    while i < len(arg_list):
        if arg_list[i] == "--alg":
            i += 1
            my_alg = arg_list[i]
        elif arg_list[i] == "--ss":
            i += 1
            s_path = arg_list[i]
        elif arg_list[i] == "--h":
            include_h = True
            i += 1
            h_path = arg_list[i]
        elif arg_list[i] == "--check-optimistic":
            doOpt = True
        elif arg_list[i] == "--check-consistent":
            doCons = True

        i += 1

    s = open(s_path, encoding="utf8")


    line = s.readline()
    states = []
    while line != "":
        if not line.startswith("#"):
            states += [line.strip()]

        line = s.readline()

    state_o = states[0]
    good_states = states[1].split(' ')
    states = states[2:]

    transfers = {}
    for state in states:
        transitions = state.split(":")
        if (len(transitions) > 1):
            temp = transitions[1].strip().split(" ")
        else:
            temp = []
        transfers[transitions[0]] = []
        for i in range(len(temp)):
            transfers[transitions[0]] += [temp[i].split(",")]

    if include_h:
        h = open(h_path, encoding="utf8")
        line2 = h.readline()
        heur = []
        weight = {}
        
        while line2 != "":
            if not line2.startswith("#"):
                heur += [line2.strip()]

            line2 = h.readline()

        for w in heur:
            w = w.split(":")
            weight[w[0]] = float(w[1].strip())

    if my_alg == "bfs":
        solution_found, closed, ln, value, path = BFS(state_o, good_states, transfers)
        print("# BFS")
        print("[FOUND_SOLUTION]:", "yes" if solution_found else "no")
        print("[STATES_VISITED]:", str(len(closed)))
        print("[PATH_LENGTH]:", str(ln))
        print("[TOTAL_COST]:", value)
        print("[PATH]:", path)

    elif my_alg == "ucs":
        solution_found, closed, ln, value, path = UCS(state_o, good_states, transfers)
        print("# UCS")
        print("[FOUND_SOLUTION]:", "yes" if solution_found else "no")
        print("[STATES_VISITED]:", str(len(closed)))
        print("[PATH_LENGTH]:", str(ln))
        print("[TOTAL_COST]:", value)
        print("[PATH]:", path)

    elif my_alg == "astar" and h_path != "":
        solution_found, closed, ln, value, path = A_STAR(state_o, good_states, transfers, weight)
        print("# A-STAR", h_path)
        print("[FOUND_SOLUTION]:", "yes" if solution_found else "no")
        print("[STATES_VISITED]:", str(len(closed)))
        print("[PATH_LENGTH]:", str(ln))
        print("[TOTAL_COST]:", value)
        print("[PATH]:", path)

    if doOpt and h_path != "":
        return_val = isOptimisticH(transfers, weight, good_states)
        print("# HEURISTIC-OPTIMISTIC", h_path)
        print(return_val)

    if doCons and h_path != "":
        return_val = isConsistentH(transfers, weight)
        print("# HEURISTIC-CONSISTENT", h_path)
        print(return_val)











