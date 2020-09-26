floor = [230, 77, 222, 3, 22, 236, 194, 224]
floor = floor[::-1]
count = 0
while floor:
    if len(floor)==1:
        print(count,floor[-1])
        if floor[-1]%2 == 0:
            count+= (2* floor[-1])
        else:
            count+= (2* floor[-1]) +1
        
        break
    count+= floor[-1]*2+1
    if floor[-1]>=floor[-2]:
        if (floor[-1]-floor[-2])%2==0:
            floor[-2] = 1
            floor.pop()
        else:
            floor.pop()
            floor.pop()
            count+=1
            floor[-1] -=1
    else:
        floor[-2]-=floor[-1]
        floor[-2]-=1
        floor.pop()
