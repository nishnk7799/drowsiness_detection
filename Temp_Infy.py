instr = input()
s = []
t = 0
v = ['a','e','i','o','u']
vf = 0
cf = 0
for i in range(len(instr)):
    ss = ''
    for j in range(i,len(instr)):
        if instr[i] in v:
            if vf == 0:
                if instr[j] not in v:
                    vf = 1
                    ss += instr[j]
                    continue
            else:
                if instr[j] in v:
                    vf = 1
                    ss += instr[j]
                    continue
        else:
            if cf == 0:
                if instr[j] not in v:
                    cf = 1
                    ss += instr[j]
                    continue
            else:
                if instr[j]  in v:
                    cf = 0
                    ss += instr[j]
                    continue
    s.append(ss)
    vf = 0
    cf = 0
m = 0
for i in s:
    if m < len(i):
        m = len(i)
i =0
while i < len(s):
    if len(s[i]) != m:
        s.remove(s[i])
    else:
        i+=1
sum = []
for i in s:
    k = 0
    for j in i:
        k += ord(j)
    sum.append(k)
m =max(sum)
for i in range(len(sum)):
    if sum[i] == m and len(s[i])>3:
        print(s[i])
        exit()
print('X')