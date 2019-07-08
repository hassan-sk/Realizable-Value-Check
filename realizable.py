# Assignment 3
# Muhammad Hassan Sheikh - 13030

import numpy as np
import random

def main():
    # there was no input requirement so I made it so that a random A and T
    # is made which is then fed to the function
    n = 20
    array = []
    T = random.randint(1,1001)
    randomArrayStr = ""
    for i in range(n):
        x = random.randint(1,101)
        randomArrayStr += str(x)+" "
        array.append(x)
    print("n = "+str(n))
    print("\nThe input array:")
    print(randomArrayStr)
    print("\nT = "+str(T))
    print("\nPart 1: Realizability check")
    realizable(array,T)
    print("\nPart 2: One solution")
    showone(array,T)
    print("\nPart 3: All solutions")
    showall(array,T)

class Node:
    # I have use a tree for finding all solutions
    # this is the class for the tree
    def __init__(self,value,coordinates,parent):
        self.value = value
        self.coordinates = coordinates
        self.parent = parent

def realizable(A,T):
    
    MaxSum = 0
    for i in A: # calculation of Maxsum
        MaxSum+=i
    if (abs(T) > MaxSum):  # if T > maxsum of T < -maxsum then function exits
        print("The value "+str(T)+" is not realizable")
        return False
    matrix = [[0 for x in range(len(A))] for y in range((2*MaxSum)+1)] # the creation of array, filled with 0
    values = set({0}) # current set of values discovered
    values_new =  set({}) # new set of discovered values
    for j in range(len(A)):
        for i in range(len(matrix)):
            if (((i-MaxSum)-A[j]) in values):
                values_new.add(i-MaxSum)
                matrix[i][j] = -1
            elif (((i-MaxSum)+A[j]) in values):
                values_new.add(i-MaxSum)
                matrix[i][j] = 1
        values = values_new # current set is reset to new values
        values_new = set({}) # new set is reinitialized
    if(matrix[T+MaxSum][len(A)-1] != 0): # finally, if there is value at last index then it is realizable
        print("The value "+str(T)+" is realizable")
        return True
    else: 
        print("The value "+str(T)+" is not realizable")
        return False
    
def showone(A,T):
    MaxSum = 0
    for i in A:
        MaxSum+=i
    if (abs(T) > MaxSum): 
        print("The value "+str(T)+" is not realizable")
        return False
    matrix = [[0 for x in range(len(A))] for y in range((2*MaxSum)+1)]
    values = set({0})
    values_new =  set({})
    for j in range(len(A)):
        for i in range(len(matrix)):
            if (((i-MaxSum)-A[j]) in values):
                values_new.add(i-MaxSum)
                matrix[i][j] = -1
            elif (((i-MaxSum)+A[j]) in values):
                values_new.add(i-MaxSum)
                matrix[i][j] = 1
        values = values_new
        values_new = set({})
    if(matrix[T+MaxSum][len(A)-1] == 0):
        print("The value "+str(T)+" is not realizable")
        return False
    # function same as realizable till here, below is additional work to find one path
    path = []
    steps = len(A) - 1
    point = T + MaxSum # this is the starting row value
    #we have path already in the matrix, so I will find it from there
    while(steps >=0):
        path.append(-matrix[point][steps]*A[steps]) # only the sign will be added to the path list
        point = point + A[steps]*matrix[point][steps] # using the present point we can calculate next point
        steps -=1 # the column will advance 1 step at a time
    solution = "Solution: "
    loop = len(path)-1 
    while(loop >= 0):# will run loop is reverse
        if (path[loop] >= 0):
            solution+="+"+str(path[loop])
        else: solution+=str(path[loop])
        loop -=1 
    solution += " = "+ str(T)
    print(solution) # the solution prints
    return True

def showall(A,T):
    MaxSum = 0
    for i in A:
        MaxSum+=i
    if (abs(T) > MaxSum): 
        print("The value "+str(T)+" is not realizable")
        return False
    matrix = [[0 for x in range(len(A))] for y in range((2*MaxSum)+1)]
    values = set({0})
    values_new =  set({})
    for j in range(len(A)):
        for i in range(len(matrix)):
            # in the other 2 functions, I was not considering multiple sign possibility
            # as only 1 was enough
            # however, here I need both the sign which I am representing as 2
            if (((i-MaxSum)-A[j]) in values and ((i-MaxSum)+A[j]) in values):
                values_new.add(i-MaxSum)
                matrix[i][j] = 2            
            elif (((i-MaxSum)-A[j]) in values):
                values_new.add(i-MaxSum)
                matrix[i][j] = -1
            elif (((i-MaxSum)+A[j]) in values):
                values_new.add(i-MaxSum)
                matrix[i][j] = 1
        values = values_new
        values_new = set({})
    if(matrix[T+MaxSum][len(A)-1] == 0):
        print("The value "+str(T)+" is not realizable")
        return False
    # the code above it same as the other 2 functions except the 1 change
    # To find all paths I have used a tree
    # I start with the root of the tree that I have initialized below
    result = Node(T,None,None)
    # below it the first sign node
    head = Node(matrix[MaxSum+T][len(A)-1],[MaxSum+T,len(A)-1],result)
    # the list below contains all the unexplored nodes
    unexplored = [head]
    # leads contains all the leaf nodes that are leading to the path
    leads = []
    i = 0
    while True:
        if (unexplored == []): break # the loop stops stops all nothing is left to explore
        node = unexplored.pop() # starts with popping the last node from the list
        if (node.coordinates[1] == 0): # is y coordinate is 0 means we have reached solution
            leads.append(node) # the node is added to the list
        else:
            value = node.value # the value from the node is taken into consideration
            if value == 2: # when it has both signs
                # 2 new nodes are added to the list with specified - and + signs
                unexplored.append(Node(-1,node.coordinates,node.parent))
                unexplored.append(Node(1,node.coordinates,node.parent))
            elif value == -1: # in case sign is +
                newNode = matrix[node.coordinates[0]-A[node.coordinates[1]]][node.coordinates[1]-1]
                unexplored.append(Node(newNode,[node.coordinates[0]-A[node.coordinates[1]],node.coordinates[1]-1],node))
            elif value == 1:# in case sign is -
                newNode = matrix[node.coordinates[0]+A[node.coordinates[1]]][node.coordinates[1]-1]
                unexplored.append(Node(newNode,[node.coordinates[0]+A[node.coordinates[1]],node.coordinates[1]-1],node))
    # once all the possible solutions are discovered I start printing as seen below
    for i in range(len(leads)):
        output = "Sol " + str(i+1).zfill(len(str(len(leads)))) +" : "
        head = leads[i]
        while True:
            if (head.coordinates != None):
                if (head.value == 1):    
                    output += "-"+str(A[head.coordinates[1]])
                if (head.value == -1):    
                    output += "+"+str(A[head.coordinates[1]])
            head = head.parent
            if head == None: break
        output += " = " + str(T)
        print(output)
    return True
            

if __name__== "__main__":
    main()
