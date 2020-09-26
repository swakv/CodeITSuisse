import numpy as np
# data = {'number_of_salads': 8, 'salad_prices_street_map': 
# [['3', '15', 'X', '11', '20', '9', 'X', '15', '20', '1', '7', '16', '4', '9', '5', '15', '12', '19', '14', '9', '15', '10', 'X'], 
# ['X', '11', '13', 'X', 'X', '5', '1', '18', '17', 'X', 'X', 'X', '17', '5', '16', '7', '16', '2', '9', '17', 'X', '18', '20'], 
# ['X', '14', '10', '9', '18', '1', '6', '2', '10', 'X', '10', 'X', '15', '19', 'X', 'X', '6', '6', '7', '16', 'X', 'X', '17'], 
# ['18', '4', '4', '2', '7', 'X', '1', '1', '2', 'X', '11', '9', '20', 'X', 'X', 'X', 'X', '11', '7', '1', '17', '14', 'X'], 
# ['3', 'X', '5', 'X', '1', '10', '16', '18', 'X', '15', '8', '17', 'X', '10', '19', '8', '5', '5', 'X', '10', 'X', 'X', '18'], 
# ['10', '2', '15', 'X', '11', '12', '9', '5', '2', '11', '5', '14', '3', '6', '10', '4', '18', '5', '4', '18', 'X', '14', '13'], 
# ['9', 'X', '14', '8', '11', '20', '1', 'X', 'X', '1', 'X', '3', '7', 'X', '5', 'X', '18', '17', 'X', '3', '16', '19', 'X']]}

data = {
    "number_of_salads" : 3,
    "salad_prices_street_map" : [["12", "12", "3", "X", "3"], ["23", "X", "X", "X", "3"], ["33", "21", "X", "X", "X"], ["9", "12", "3", "X", "X"], ["X", "X", "X", "4", "5"]]
}
n = data["number_of_salads"]
arr = data["salad_prices_street_map"]
arr_int = arr

for i in range(len(arr)):
    for j in range(len(arr[i])):
        if arr[i][j] == "X":
            arr_int[i][j] = np.inf
        else:
            arr_int[i][j] = int(arr[i][j])

arr_sum = []

# arr = np.array([10, 20, 30, 40, 50])
for i in range(len(arr_int)):
    sums  = np.convolve(arr_int[i], np.ones(n, dtype=np.int), mode='valid')
    print(sums)
    arr_sum+=list(sums)
# print(arr_sum)
arr_sum = np.array(arr_sum)
min_val = arr_sum.min()
if min_val == np.inf:
    ans = 0
else:
    ans = min_val
ans = int(ans)
print(ans)