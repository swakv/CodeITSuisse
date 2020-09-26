
import logging
import json
import heapq
from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


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
    if len(allSequence) == 0:
        return None
    path = allSequence[0]
    # print(path[0])
    for element in path[0][::-1]:
        if element[0] == "+":
            oriA = oriA[:element[1]+1] + "+" + oriB[element[2]]+ oriA[1+element[1]:]
        elif element[0] == "-":
            oriA = oriA[:element[1]] + "-"+ oriA[element[1]:]
        else:
            oriA = oriA[:element[1]]+oriB[element[2]]+ oriA[1+element[1]:] 
    return len(path[0]),oriA


@app.route('/inventory-management', methods=['POST'])
def evaluateIM():
    data = request.get_json()
    # logging.info("data sent for evaluation {}".format(data))
    answers = []
    for case in data:
        values = []
        query_string = case["searchItemName"]
        database = case["items"]
        for item in database:
            heapq.heappush(values, listAllSequence(query_string,item))
        # values = sorted(values,key = lambda x:x[0])[:10]
        values = values.sort()
        if values == None:
            answers.append({"searchItemName":query_string, "searchResult":""})
        else:
            answers.append({"searchItemName":query_string, "searchResult":list(map(lambda x:x[1],values))
        })
    result = answers
    logging.info("My result :{}".format(result))
    return json.dumps(result)
