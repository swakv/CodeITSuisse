data = {
    "infected": {
        "name":"plastic",
        "genome":"acg-gcu-uca-gca-acu-ccc-gua-acg-gcu-uca-gca-acu-cac-gaa"
    },
    "origin": {
        "name":"metal",
        "genome":"acg-acu-uca-gca-acu-ccc-gua-acg-ccu-uca-gca-acu-cac-gac"
    },
    "cluster":[
        {
            "name":"thread",
            "genome":"acg-acu-uca-gca-acu-ccc-gua-acg-ccu-uca-gca-acu-cac-gaa"
        }
    ]
}

data = {'infected': {'name': 'apple', 'genome': 'acg-gcu-uca-gca-acu-ccc-gua-acg-gcu-uca-gca-acu-cac-gaa'}, 
'origin': {'name': 'banana', 'genome': 'ccg-ccu-uca-gca-acu-ccc-gua-acg-gcu-uca-gca-acu-cac-gaa'}, 
'cluster': [
    {'name': 'mango', 'genome': 'ccg-ccu-uca-gca-acu-ccc-gua-acg-gcu-uca-gca-acu-cac-gaa'}, 
    {'name': 'grape', 'genome': 'ccg-ccu-uca-gca-acu-ccc-gua-acg-gcu-uca-gca-acu-cac-gaa'}, 
    {'name': 'orange', 'genome': 'ccg-ccu-uca-gca-acu-ccc-gua-acg-gcu-uca-gca-acu-cac-gaa'}, 
    {'name': 'pineapple', 'genome': 'ccg-ccu-uca-gca-acu-ccc-gua-acg-gcu-uca-gca-acu-cac-gaa'},
    {'name': 'strawberry', 'genome': 'ccg-ccu-uca-gca-acu-ccc-gua-acg-gcu-uca-gca-acu-cac-gaa'}, 
    {'name': 'jackfruit', 'genome': 'ccg-ccu-uca-gca-acu-ccc-gua-acg-gcu-uca-gca-acu-cac-gaa'}
    ]
}
import numpy as np


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
    # print(path[0])
    
    return len(path[0]), path[0]

for i in range(len(data["cluster"])):
        if len(data["cluster"]) != 0:
            str1 = data["infected"]["genome"]
            str2 = data["origin"]["genome"]
            # ITERATE THROUGH CLUSTERS ALSO 
            str3 = data["cluster"][i]["genome"]
            sim1, path1 = listAllSequence(str1, str2)
            sim2, path2 = listAllSequence(str2, str3)

            print(path1)

            output = []

            if (sim1 == sim2):
                if len(path1) > 1:
                    str_name = data["infected"]["name"] + "*" + "->" + data["origin"]["name"]
                else:
                    str_name = data["infected"]["name"] + "->" + data["origin"]["name"]
                output.append(str_name)
                if  > 1:
                    str_name = data["infected"]["name"] + "*" + "->" + data["cluster"][i]["name"]
                else:
                    str_name = data["infected"]["name"] + "->" + data["cluster"][i]["name"]
                output.append(str_name)

            elif sim1 > sim2:
                if sim1 > 1:
                    str_name = data["infected"]["name"] + "*" + "->" + data["cluster"][i]["name"] + "->" + data["origin"]["name"]
                elif sim2 > 1:
                    str_name = data["infected"]["name"] + "->" + data["cluster"][i]["name"] + "*"+ "->" + data["origin"]["name"]
                else:
                    str_name = data["infected"]["name"] + "->" + data["cluster"][i]["name"] + "->" + data["origin"]["name"]
                
                output.append(str_name)
            else:
                if sim1>1:
                    str_name = data["infected"]["name"] + "*"+ "->" + data["origin"]["name"]
                else:
                    str_name = data["infected"]["name"] + "->" + data["origin"]["name"]
                output.append(str_name)
        else:
            str1 = data["infected"]["genome"]
            str2 = data["origin"]["genome"]
            sim1 = listAllSequence(str1, str2)

            output = []

            if sim1 > 1:
                str_name = data["infected"]["name"] + "*" + "->" + data["origin"]["name"]
            else:
                str_name = data["infected"]["name"] + "->" + data["origin"]["name"]
            output.append(str_name)

print(output)