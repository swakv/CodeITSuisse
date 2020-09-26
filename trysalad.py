import numpy as np

n = 3
arr = [["X", "X", "2"], ["2", "3", "X"], ["X", "3", "2"]]
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
    arr_sum.append(sums)

arr_sum = np.array(arr_sum)
min_val = arr_sum.min()
if min_val == np.inf:
    ans = 0
else:
    ans = min_val

print(ans)