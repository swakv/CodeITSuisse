input = [{"searchItemName":"Samsung Aircon","items":["Smsng Auon","Amsungh Aircon","Samsunga Airon"]}]

# import numpy as np

# def levenshtein(seq1, seq2):
#     size_x = len(seq1) + 1
#     size_y = len(seq2) + 1
#     matrix = np.zeros ((size_x, size_y))
#     for x in range(size_x):
#         matrix [x, 0] = x
#     for y in range(size_y):
#         matrix [0, y] = y

#     for x in range(1, size_x):
#         for y in range(1, size_y):
#             if seq1[x-1] == seq2[y-1]:
#                 matrix [x,y] = min(
#                     matrix[x-1, y] + 1,
#                     matrix[x-1, y-1],
#                     matrix[x, y-1] + 1
#                 )
#             else:
#                 matrix [x,y] = min(
#                     matrix[x-1,y] + 1,
#                     matrix[x-1,y-1] + 1,
#                     matrix[x,y-1] + 1
#                 )
#     print (matrix)
#     return (matrix[size_x - 1, size_y - 1])

# levenshtein("Samsung Aircon", "Smsng Auon")

import numpy as np
import sys

def getMemorizationMatrix(StringA,StringB):
    matrix = np.zeros([len(StringA)+1,len(StringB)+1])
    
    for j in range(0,len(StringB)+1):
        matrix[0][j] = j
    
    for i in range(0,len(StringA)+1):
        matrix[i][0] = i
        
    for i in range(1,len(StringA)+1):
        for  j in range(1,len(StringB) + 1):
            if(StringA[i-1]==StringB[j-1]):
                matrix[i][j] = matrix[i-1][j-1]
            else:
                matrix[i][j] = np.min([matrix[i-1][j],matrix[i-1][j-1],matrix[i][j-1]])+1
    
    return matrix

def backtrackSequence(matrix,  StringA, StringB, i=None, j=None):
    if(i==None):
        i = len(StringA)
    if(j==None):
        j = len(StringB)
    if(i==0 and j==0):
        return [[[],StringA,0]]
    if(i>=0 and j>=0 and StringA[i-1] == StringB[j-1]):
        paths = backtrackSequence(matrix,StringA,StringB,i-1,j-1)
        return paths
    else:
        paths = []
        if(matrix[i-1][j] + 1 == matrix[i][j] and i-1 >= 0):
            allPaths = backtrackSequence(matrix,StringA,StringB, i-1,j)
            for path in allPaths:
                cS = path[1]
                deviation = path[2]
                path[1] = cS[0:i+deviation-1] + cS[i+deviation:len(cS)]
                path[2] = deviation - 1
                #print(cS + " delete " + StringA[i-1] + " " + path[1] + " " + "("+str(i)+","+str(j)+")")
                path[0].append(("-" ,i-1))
            paths.extend(allPaths)
            #print('Paths',paths)
        if(matrix[i][j-1] + 1 == matrix[i][j] and j-1 >= 0):
            allPaths = backtrackSequence(matrix,StringA,StringB, i,j-1)
            for path in allPaths:
                cS = path[1]
                deviation = path[2]
                path[1] = cS[0:i+deviation] + StringB[j-1] + cS[i+deviation:len(cS)]
                path[2] = deviation + 1
                path[0].append(("+",i-1,j-1))
            paths.extend(allPaths)
            #print('Paths',paths)
        if(matrix[i-1][j-1] + 1 == matrix[i][j] and i-1 >= 0 and j-1 >= 0):
            allPaths = backtrackSequence(matrix,StringA,StringB,i-1,j-1)
            for path in allPaths:
                cS = path[1]
                deviation = path[2]
                path[1] = cS[0:i+deviation-1] + StringB[j-1] + cS[i+deviation:len(cS)]
                # path[0].append(cS + " replace " + StringA[i-1]  + " with " + StringB[j-1] +  "("+str(i-1+deviation)+")")
                path[0].append(("r",i-1,j-1))
            paths.extend(allPaths)
            # print('Paths',paths)
        return paths

def listAllSequence(StringA,StringB):
    oriA = StringA
    oriB = StringB
    StringA = StringA.lower()
    StringB = StringB.lower()
    matrix = getMemorizationMatrix(StringA,StringB)
    allSequence = backtrackSequence(matrix,StringA,StringB)
    path = allSequence[0]
    print(path[0])
    for element in path[0][::-1]:
        if element[0] == "+":
            oriA = oriA[:element[1]+1] + "+" + oriB[element[2]]+ oriA[1+element[1]:]
        elif element[0] == "-":
            oriA = oriA[:element[1]] + "-"+ oriA[element[1]:]
        else:
            oriA = oriA[:element[1]]+oriB[element[2]]+ oriA[1+element[1]:] 
    print(oriA)
    # for path in allSequence:
    #     print(len(path[0]))
        # if(len(path[0])>0):
        #     print(path[0])
        #     print(" -> ".join(path[0])," -> ",path[1])
        # else:
        #     print(StringA," -> ",StringB)

listAllSequence("Samsung Aircon", "Amsungh Aircon")