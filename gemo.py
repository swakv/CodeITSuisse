def gmo(string):
    arr = []
    structures = {
        "ACGT" : 0,
        "CC": 0,
        "AACGT": 0,
        "AA":0,
        "AAG": 0,
        "AAT": 0,
        "AT":0,
        "AG":0,
        "A":0
    }
    counts = {"A": 0, "C": 0, "G": 0, "T": 0}
    for letter in string:
        counts[letter] += 1
    # print(counts)
    num_acgt = min(counts["A"], counts["C"], counts["T"], counts["G"])
    structures["ACGT"] = num_acgt
    leftover_a = counts["A"]-num_acgt
    leftover_c = counts["C"]-num_acgt
    leftover_g = counts["G"]-num_acgt
    leftover_t = counts["T"]-num_acgt
    
    if leftover_c % 2 == 1:
        if structures["ACGT"] > 0:
            structures["ACGT"] -=1  
            structures["CC"] += 1
            leftover_a += 1
            leftover_g += 1
            leftover_t += 1
    
    structures["CC"] += leftover_c//2
    leftover_c = 0

    temp = min(leftover_t, leftover_a//2)
    leftover_a -= 2*temp
    leftover_t -= temp
    structures["AAT"] = temp

    temp = min(leftover_g, leftover_a//2)
    leftover_a -= 2*temp
    leftover_g -= temp
    structures["AAG"] = temp

    right_side = max(0, leftover_a - 2)
    temp = leftover_a - right_side
    if temp == 1:
        structures["A"] = 1
    elif temp == 2:
        structures["AA"] = 1
    
    leftover_a = max(0, leftover_a - 2) # right side

    temp = min(structures["ACGT"],leftover_a)
    structures["ACGT"]-= temp
    leftover_a -= temp
    structures["AACGT"] = temp

    temp = min(structures["CC"],leftover_a//2)
    structures["CC"]-=temp
    leftover_a -= 2*temp
    structures["AACC"] = temp
    if leftover_t:
        structures["T"] = leftover_t
    if leftover_g:
        structures["G"] = leftover_g
    if leftover_a:
        structures["A"] += leftover_a
    # while True:
    #     if leftover_a//3 == 0:
    #         break
    #     if structures

    # print(leftover_a, leftover_c, leftover_g, leftover_t)
    # print(structures)
    return construct_output(structures)

def construct_output(structures):
    if "AA" in structures:
        end = "AA"
        del structures["AA"]
    elif "A" in structures:
        end = "A"
        del structures["A"]
    
    accum = ""
    for key, value in structures.items():
        accum+= key*value
    
    accum+=end
    return accum
print(gmo('AAACCCAAAGGTTACTGAAAAG'))