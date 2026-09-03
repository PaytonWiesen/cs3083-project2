import heapq
import numpy
import matplotlib.pyplot
import time
import os
import json

def backtrackingSearch(state):
    possibleValues = {}
    for ind,i in enumerate(state):
        for jin, j in enumerate(state[ind]):
            possibleValues.update(findPossibleValues(state,ind,jin))

    return backtrack(state,possibleValues)

def bruteForceBacktrackingSearch(state):
    possibleValues = {}
    for ind,i in enumerate(state):
        for jin, j in enumerate(state[ind]):
            possibleValues.update(findPossibleValues(state,ind,jin))

    return bruteForceBacktrack(state,possibleValues)

def bruteForceBacktrack(state, possibleValues):
    state = state.copy()
    if checkSolution(state):
        return state
    var = -1
    for ind, i in enumerate(state):
        for jin, j in enumerate(state):
            if state[ind][jin] == 0:
                var = (ind,jin)
                break
        if var != -1:
            break
    for value in possibleValues.get(var):
        newState = state.copy()
        newState[var[0]][var[1]] = value
        if checkConsistency(newState):
            newValues = dictionaryCopy(possibleValues)
            newValues = inferFC(newState,newValues,var)
            if not checkFailure(newState,newValues):
                result = bruteForceBacktrack(newState,newValues)
                if result is not None:
                    return result
            newState[var[0]][var[1]] = 0
    return None

def backtrack(state,possibleValues):
    state = state.copy()
    if checkSolution(state):
        return state
    var = selectUnassignedVariable(state,possibleValues)
    for value in orderDomainValues(state,possibleValues,var):
        newState = state.copy()
        newState[var[0]][var[1]] = value
        if checkConsistency(newState):
            inferences = inferMAC(state,dictionaryCopy(possibleValues),var)
            if not checkFailure(newState,inferences):
                result = backtrack(newState,inferences)
                if result is not None:
                    return result
            newState[var[0]][var[1]] = 0
    return None

def checkFailure(state,possibleValues):
    for key in possibleValues:
        if len(possibleValues.get(key)) == 0:
            return True
    return False

def dictionaryCopy(dictionary):
    # .copy() doesnt prevent lists in values from changing upon modification of one
    dictCopy = {}
    for key in dictionary:
        value = dictionary.get(key)
        l = []
        for i in value:
            l.append(i)
        dictCopy[key] = l
    return dictCopy

def findPossibleValues(state,i,j):
    possibleValues = {}
    size = int(len(state)**0.5)
    options = list(range(1,len(state)+1))
    for rin,r in enumerate(state):
        if state[rin][j] in options and rin != i:
            options.remove(state[rin][j])
    for cin,c in enumerate(state[i]):
        if state[i][cin] in options and cin != j:
            options.remove(state[i][cin])
    for rin, r in enumerate(range(0,size)):
        for cin, c in enumerate(range(0,size)):
            if state[size*int(i/size)+rin][size*int(j/size)+cin] in options and (size*int(i/size)+rin != i or size*int(j/size)+cin != j):
                if state[size*int(i/size)+rin][size*int(j/size)+cin] in options:
                    options.remove(state[size*int(i/size)+rin][size*int(j/size)+cin])
                
    possibleValues[(i,j)] = options
    return possibleValues

def selectUnassignedVariable(state,possibleValues):
    lowest = None
    lowestOptions = float('inf')
    for key in possibleValues:
        if len(possibleValues.get(key)) < lowestOptions and state[key[0]][key[1]] == 0:
            lowest = key
            lowestOptions = len(possibleValues.get(key))

    return lowest

def orderDomainValues(state,possibleValues,var):
    l = possibleValues.get(var)
    size = int(len(state)**0.5)
    valueCount = {}
    if l == None:
        return []
    for c in l:
        valueCount[c] = 0
    for ind, i in enumerate(state):
        for c in l:
            if c in possibleValues[(ind,var[1])] and ind != var[0]:
                valueCount[c]+=1
    for jin, j in enumerate(state[ind]):
        for c in l:
            if c in possibleValues[(var[0],jin)] and jin != var[1]:
                valueCount[c]+=1
    for ind, i in enumerate(range(0,size)):
        for jin, j in enumerate(range(0,size)):
            for c in l:
                if ((size*int(var[0]/size)+ind) != var[0] or (size*int(var[1]/size)+jin) != var[1]) and c in possibleValues[((size*int(var[0]/size)+ind),(size*int(var[1]/size)+jin))]:
                    valueCount[c]+=1

    sortedValues = dict(sorted(valueCount.items(), key=lambda item: item[1]))
    l = []
    for key in sortedValues:
        l.append(key)
    return l

def inferFC(state,possibleValues,var):
    size = int(len(state)**0.5)
    value = state[var[0]][var[1]]
    for ind, i in enumerate(state):
        if ind != var[0]:
            l = possibleValues.get((ind,var[1]))
            if value in l:
                l.remove(value)      
            possibleValues[(ind,var[1])] = l
    for ind, i in enumerate(state):
        if ind != var[1]:
            l = possibleValues.get((var[0],ind))
            if value in l:
                l.remove(value)
            possibleValues[(var[0],ind)] = l
    for rin, r in enumerate(range(0,size)):
        for cin, c in enumerate(range(0,size)):
            if (size*int(var[0]/size)+rin) != var[0] or (size*int(var[1]/size)+cin) != var[1]:
                l = possibleValues.get((size*int(var[0]/size)+rin,size*int(var[1]/size)+cin))
                if value in l:
                    l.remove(value)
                possibleValues[(size*int(var[0]/size)+rin,size*int(var[1]/size)+cin)] = l

    return possibleValues

def inferMAC(state, possibleValues, var):
    l = []
    for ind, i in enumerate(state):
        if ind != var[0]:
            l.append((ind,var[1]))
    for ind, i in enumerate(state):
        if ind != var[1]:
            l.append((var[0],ind))
    size = int(len(state)**0.5)
    for ind,i in enumerate(range(0,size)):
        for jin,j in enumerate(range(0,size)):
            if (size*int(var[0]/size)+ind) != var[0] or (size*int(var[1]/size)+jin) != var[1]:
                l.append((size*int(var[0]/size)+ind,size*int(var[1]/size)+jin))

    while l:
        r, c = l.pop()
        if state[var[0]][var[1]] in possibleValues[(r,c)]:
            possibleValues[(r,c)].remove(state[var[0]][var[1]])
            if not possibleValues[(r,c)]:
                return {}
            if len(possibleValues[(r,c)]) == 1:
                v = possibleValues[(r,c)][0]
                state[r][c] = v
                res = inferMAC(state, possibleValues, (r,c))
                if res is False:
                    return {}
                state[r][c] = 0

    return possibleValues

def checkSolution(state):
    for ind,i in enumerate(state):
        check = []
        for jin, j in enumerate(state[ind]):
            if state[ind][jin] in check or state[ind][jin] == 0:
                return False
            check.append(j)
        
    for ind,i in enumerate(state[0]):
        check = []
        for jin, j in enumerate(state):
            if state[ind][jin] in check or state[ind][jin] == 0:
                return False
            check.append(j)

    size = int(len(state)**0.5)
    for ind,i in enumerate(range(0,size)):
        for jin,j in enumerate(range(0,size)):
            check = []
            for rin,r in enumerate(range(0,size)):
                for cin,c in enumerate(range(0,size)):
                    if state[ind*size+rin][jin*size+cin] in check and state[ind*size+rin][jin*size+cin] == 0:
                        return False
                    check.append(state[ind*size+rin][jin*size+cin])

    return True

def checkConsistency(state):
    for ind,i in enumerate(state):
        check = []
        for jin, j in enumerate(state[ind]):
            if state[ind][jin] in check and state[ind][jin] != 0:
                return False
            check.append(j)
        
    for ind,i in enumerate(state[0]):
        check = []
        for jin, j in enumerate(state):
            if state[ind][jin] in check and state[ind][jin] != 0:
                return False
            check.append(j)

    size = int(len(state)**0.5)
    for ind, i in enumerate(range(0,size)):
        for jin, j in enumerate(range(0,size)):
            check = []
            for rin,r in enumerate(range(0,size)):
                for cin,c in enumerate(range(0,size)):
                    if state[ind*size+rin][jin*size+cin] in check and state[ind*size+rin][jin*size+cin] != 0:
                        return False
                    check.append(state[ind*size+rin][jin*size+cin])
    return True



with open('sudoku9.json', 'r') as f:
    board = json.load(f)
displayOriginalBoard = numpy.array(board)
print(displayOriginalBoard)

t = time.time()
print(numpy.array(backtrackingSearch(board.copy())))
print(time.time()-t)
t = time.time()
print(numpy.array(bruteForceBacktrackingSearch(board.copy())))
print(time.time()-t)