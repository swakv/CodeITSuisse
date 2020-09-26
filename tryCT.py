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

import numpy as np

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    # print (matrix)
    return (matrix, matrix[size_x - 1, size_y - 1])

str1 = data["infected"]["genome"]
str2 = data["origin"]["genome"]
# ITERATE THROUGH CLUSTERS ALSO 
str3 = data["cluster"][0]["genome"]
sim1, matrix = levenshtein(str1, str2)
sim2, matrix = levenshtein(str2, str3)

output = []

if (sim1 == sim2):
    str_name = data["infected"]["name"] + "->" + data["origin"]["name"]
    output.append(str_name)
    str_name = data["infected"]["name"] + "->" + data["cluster"]["name"]
    output.append(str_name)
elif sim1 > sim2:
    str_name = data["infected"]["name"] + "->" + data["cluster"][0]["name"] + "->" + data["origin"]["name"]
    output.append(str_name)
else:
    str_name = data["infected"]["name"] + "->" + data["origin"]["name"]
    output.append(str_name)

print(output)