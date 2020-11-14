from itertools import takewhile
import sys
sys.setrecursionlimit(1500)


# main
# gram = {
# 	"S":["AB"],
# 	"A":["a","\u03B5"],
# 	"B":["b","\u03B5"]
# }


# gram = {
# 	"S":["ABC"],
# 	"A":["abA","ab"],
# 	"B":["BC","b"],
# 	"C":["c","cC"]
# }

gram = {
    "S": ["aABb"],
    "A": ["c", "\u03B5"],
    "B": ["d", "\u03B5"]
}

# into dict


def toDict(prod):
    gam = {}
    temp = ''
    for p in prod:
        Prodruleslist = []
        RHS = []
        split = p.split("->")
        LHS = split[0]
        for i in split[1].split("|"):

            Prodruleslist.append(i)
        for l in Prodruleslist:
            li = list(l)

            for check in range(0, len(li)):

                if(li[check] == "'"):
                    temp = li[check-1]
                    li[check-1] = temp + "'"
                    li.remove("'")
            RHS.append(li)
        gam[LHS] = RHS
    return gam

# into string


def toList(prod):
    gam = []
    for k in prod:
        string = str(k) + '->'
        RHS = ''
        for rule in prod[k]:
            join = ''
            RHS += ('|' + join.join(rule))
        string += RHS[1:]
        gam.append(string)
    return gam


def removeDirectLR(gramA, A):
    temp = gramA[A]
    tempCr = []
    tempInCr = []
    for i in temp:
        if i[0] == A:
            tempInCr.append(i[1:]+[A+"'"])
        else:
            tempCr.append(i+[A+"'"])
    tempInCr.append(["\u03B5"])
    gramA[A] = tempCr
    gramA[A+"'"] = tempInCr
    return gramA


def checkForIndirect(gramA, a, ai):
    if ai not in gramA:
        return False
    if a == ai:
        return True
    for i in gramA[ai]:
        if i[0] == ai:
            return False
        if i[0] in gramA:
            return checkForIndirect(gramA, a, i[0])
    return False


def rep(gramA, A):
    temp = gramA[A]
    newTemp = []
    for i in temp:
        if checkForIndirect(gramA, A, i[0]):
            t = []
            for k in gramA[i[0]]:
                t = []
                t += k
                t += i[1:]
                newTemp.append(t)

        else:
            newTemp.append(i)
    gramA[A] = newTemp
    return gramA


def rem(gram):
    c = 1
    conv = {}
    gramA = {}
    revconv = {}
    for j in gram:
        conv[j] = "A"+str(c)
        gramA["A"+str(c)] = []
        c += 1
    for i in gram:
        for j in gram[i]:
            temp = []
            for k in j:
                if k in conv:
                    temp.append(conv[k])
                else:
                    temp.append(k)
            gramA[conv[i]].append(temp)
    for i in range(c-1, 0, -1):
        ai = "A"+str(i)
        for j in range(0, i):
            aj = gramA[ai][0][0]
            if ai != aj:
                if aj in gramA and checkForIndirect(gramA, ai, aj):
                    gramA = rep(gramA, ai)

    for i in range(1, c):
        ai = "A"+str(i)
        for j in gramA[ai]:
            if ai == j[0]:
                gramA = removeDirectLR(gramA, ai)
                break

    op = {}
    for i in gramA:
        a = str(i)
        for j in conv:
            a = a.replace(conv[j], j)
        revconv[i] = a

    for i in gramA:
        l = []
        for j in gramA[i]:
            k = []
            for m in j:
                if m in revconv:
                    k.append(m.replace(m, revconv[m]))
                else:
                    k.append(m)
            l.append(k)
        op[revconv[i]] = l

    return op


def getLeftFactoring(gam={}):
    LF = {}
    for k in gam:
        if(len(gam[k]) > 1):
            for t in range(0, len(gam[k])-1):
                if(gam[k][t][0] == gam[k][t+1][0]):
                    LF[k] = gam[k]
                    break
    return LF

# FOR LEFT FACTORING
def prefix(x):
    return len(set(x)) == 1


def removeLeftFactorial(s):
    while(True):
        rules = []
        common = []
        split = s.split("->")
        starting = split[0]
        for i in split[1].split("|"):
            rules.append(i)
        d = {}
        ls = [y[0] for y in rules]
        initial = list(set(ls))
        for y in initial:
            for i in rules:
                if i.startswith(y):
                    if y not in d:
                        d[y] = []
                    d[y].append(i)
        for k, l in d.items():
            r = [l[0] for l in takewhile(prefix, zip(*l))]
            common.append(''.join(r))
        for i in common:
            newalphabet = starting + "'"
            firstprod = ''
            lastprod = ''
            firstprod = starting+"->"+i+newalphabet
            index = []
            for k in rules:
                if(k.startswith(i)):
                    index.append(k)
            lastprod = newalphabet+"->"
            for j in index[:-1]:
                stringtoprint = j.replace(i, "", 1)+"|"
                if stringtoprint == "|":
                    lastprod += ("\u03B5" + "|")
                else:
                    lastprod += (j.replace(i, "", 1)+"|")
            stringtoprint = index[-1].replace(i, "", 1)+"|"
            if stringtoprint == "|":
                lastprod += "\u03B5"
            else:
                lastprod += index[-1].replace(i, "", 1)+""
            return toDict([firstprod, lastprod])
        # break


gamWithLREliminated_dict = rem(gram)
gamWithLREliminated_list = toList(gamWithLREliminated_dict)


starting = ""
rules = []
common = []

ValidGrammar_list = gamWithLREliminated_list
LeftFactorialProd = getLeftFactoring(gamWithLREliminated_dict)
LFremoved = {}
response = []

for lf in toList(LeftFactorialProd):
    ValidGrammar_list.remove(lf)
    response.append(removeLeftFactorial(lf))

ValidGrammar_dict = toDict(ValidGrammar_list)

for res in response:
    for k in res:
        ValidGrammar_dict[k] = res[k]


print("VALID GRAMMAR!")
for i in toList(ValidGrammar_dict):
    print(i)

# first
def first(gram, term):
    a = []
    if term not in gram:
        return [term]
    for i in gram[term]:
        if i[0] not in gram:
            a.append(i[0])
        elif i[0] in gram:
            a += first(gram, i[0])
    return a


firsts = {}
for i in ValidGrammar_dict:
    firsts[i] = first(ValidGrammar_dict, i)

print()
print("FIRSTs Set")
for i in firsts:
    a = ''
    print('First('+i+')'+" = {" + a.join(firsts[i]) + "}")



def follow(gram, term):
    a = []
    if(term == "S"):
        a.append("$")
    for rule in gram:
        for i in gram[rule]:
            if term in i:
                indx = i.index(term)
                if (indx+1 != len(i)):
                    try:
                        if((i[indx+1].isupper() or i[indx+1][1] == "'") and i[indx+1][1] != ["\u03B5"]):
                            a += (firsts[i[indx+1]])
                        else:

                            a += (i[indx+1])
                    except:
                        if(i[indx+1].isupper()):
                            for first in firsts[i[indx+1]]:
                                if(first != "\u03B5"):
                                    a += (firsts[i[indx+1]])
                                else:
                                    if(indx+2 != len(i)):
                                        if(i[indx+2].isupper()):
                                            for first in firsts[i[indx+2]]:
                                                a += (firsts[i[indx+2]])
                                        else:
                                            a += (i[indx+2])

                        else:
                            a += (i[indx+1])
                else:
                    if(rule in follows):
                        a += (follows[rule])
    return a


follows = {}
print()
print("FOLLOW Set")
for i in ValidGrammar_dict:
    follows[i] = follow(ValidGrammar_dict, i)
    if "\u03B5" in follows[i]:
        # print(follows[i])
        follows[i].remove("\u03B5")
    print(f'Follow({i}):', follows[i])


def getTerminalsForLL(gram={}):
    tt = []
    for key in gram:
        for prod in gram[key]:
            for ter in prod:
                if (not ter.isupper() and ter not in tt):
                    tt.append(ter)
    tt.append("$")
    return tt


table = {}
for nonTerminal in ValidGrammar_dict:
    for terminal in getTerminalsForLL(ValidGrammar_dict):
        if(terminal in firsts[nonTerminal] and terminal != "\u03B5"):
            if((nonTerminal, terminal) in table):
                print('this', (nonTerminal, terminal))
                tempprod = table[(nonTerminal, terminal)]
                if(ValidGrammar_dict[nonTerminal][0] == ['\u03B5']):
                    table[(nonTerminal, terminal)] = [
                        tempprod, ValidGrammar_dict[nonTerminal][1]]
                else:
                    table[(nonTerminal, terminal)] = [
                        tempprod, ValidGrammar_dict[nonTerminal][0]]
            else:
                table[(nonTerminal, terminal)
                      ] = ValidGrammar_dict[nonTerminal][0]
        elif(terminal == "\u03B5" and terminal in firsts[nonTerminal]):
            for fo in follows[nonTerminal]:
                if((nonTerminal, fo) in table):
                    tempprod = table[(nonTerminal, fo)]
                    table[(nonTerminal, fo)] = [tempprod, "\u03B5"]
                else:
                    table[(nonTerminal, fo)] = ["\u03B5"]
        else:
            if(terminal != "$" and (nonTerminal, terminal) not in table):
                table[(nonTerminal, terminal)] = "-"
        if((nonTerminal, terminal) not in table and terminal != "\u03B5"):
            table[(nonTerminal, terminal)] = "-"

headertt = getTerminalsForLL(ValidGrammar_dict)
headertt.remove("\u03B5")
print()
print("LL(1) Table")
for header in headertt:
    print("                    ", header, end="")
print()
print(f'{"-":-<106}')
for row in list(ValidGrammar_dict.keys()):
    print(row, end="")
    for i in headertt:
        print("                 ", table[(row, i)], end="")
    print()
    print(f'{"-":-<106}')


def push(stack, inputt):
    stack.pop(-1)
    for i in range(len(inputt)-1, -1, -1):
        stack.append(inputt[i])
    return stack


def Parse(table, string):
    INPUT = list(string+"$")
    STACK = ['$', ['S']]
    c = 0
    while STACK[-1] != INPUT[-1]:
        if(STACK[1][-1].isupper()):
            STACK[1] = push(STACK[1], table[(STACK[1][-1], INPUT[0])])
        print(STACK)
        sthDeleted = False
        while not sthDeleted:
            if(not STACK[1][-1].isupper()):
                for index in range(len(STACK[-1])-1, -1, -1):
                    if(STACK[-1][index] == INPUT[0]):
                        STACK[-1].pop(-1)
                        INPUT.pop(0)
                        sthDeleted = True
                        break
            else:
                break
            c+=1
            if(c>=50):
                break
        if(c>=50):
            print("The String is not Accepted")
            break
        if(STACK[-1] == []):
            STACK.pop(-1)
            print(STACK, INPUT)
            print("The String is ACCEPTED")
            break
        
        print(STACK, INPUT)

print()
s = "acdl"
print("PARSEING string: ", s)
Parse(table, s)


