floor = [230, 77, 222, 3, 22, 236, 194, 224]

import numpy as np
indices = [i for i, x in enumerate(floor) if x == 0]

# while np.sum(floor != 0):
# for i in range(1, len(floor)-1):

count = 0
i=0

while i < len(floor) - 1:
    if i == 0:
        floor[i+1] = floor[i+1] - 1
        count += 1
        i += 1
        continue
    if floor[i] < floor[i-1]:
        floor[i-1] = floor[i-1] - 1
        count += 1
        i -= 1
        if floor[i-1] == 0:
            break
        continue

print(floor)