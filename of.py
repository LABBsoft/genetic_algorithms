import struct
from charts import plotRosen, plotDejong
#from charts import *
heatData = [[0 for _ in range(-10,10)] for _ in range(-10,10)]
Lines = []
MAXIMUMS = {
10: 45,
11: 55,
12: 66,
13: 78,
14: 91,
15: 105,
16: 120,
17: 136,
18: 153,
19: 171,
20: 190,
21: 210,
22: 231,
23: 253,
24: 276,
25: 300,
26: 325,
27: 351
}

def bitToFloat(bits):
    if bits[1:9] == ['1','1','1','1','1','1','1','1']:
        return (100,)
    bits.reverse()
    byte = []
    temp = 0
    for i, b in enumerate(bits):
        if i % 8 == 0 and not i == 0:
            byte.append(temp)
            temp = 0
        if "1" in b:
            temp += 2 ** (i % 8)
    byte.append(temp)
    f = struct.unpack('f',bytes(byte))
    return f

def bitConvH(bits):

    n = len(bits)
    res_t = 0;
    for i in range(1, len(bits)):
        if bits[i] == '1':
            res_t += 2**(n-i-1)
    if bits[0] == '1':
        res_t = res_t - (1 << len(bits)-1)
    
    res = res_t/1000000
    return res  


def rosen_of(s):
    global heatData
    x = bitToFloat(s[:32])[0]
    y = bitToFloat(s[32:])[0]
    ans = abs(100 * pow(y - pow(x,2),2) + pow(x-1, 2))
    x = round(x)
    y = round(y)
    if x > -10 and x < 10 and y > -10 and y < 10:
        heatData[round(x) + 10][round(y) + 10] += 1
    return ans, x, y

def himmel_of(s):
    x = bitConvH(s[:24])
    y = bitConvH(s[24:])
    ans = pow(pow(x, 2)+y-11, 2) + pow(x+pow(y,2)-7,2)
    return ans, x,y

def objective_function(s):
    count = 0
    for i, c in enumerate(s):
        if c == '1':
            count += 2 ** i
    return count

def dynamic_of(s):
    a = [0]
    for char in s:
        if "0" in char:
            a.append(-1)
        else:
            a.append(int(char))
    out = MAXIMUMS[len(s)] - eval(Lines[1])
    return out, None

# Use string size divisible by 10
# Max value 
def dejong_of(s):
    fitness = 0
    x = []
    for i, c in enumerate(s):
        if i % 10 == 0:
            if i != 0:
                cur /= 100
                x.append(cur)
                fitness += cur * cur
            cur = -512
        if c == '1':
            cur += 2 ** (i % 10)
    cur /= 100
    x.append(cur)
    fitness += cur * cur
    return fitness, x, None

def useWhich():
    of = (0,0,None,True)
    userRequest = input("""Use which Objective Function?
dejong: d 
rosenbrock: r
himmelblau: h
from file: f
-> """)
    if "d" in userRequest:
        of = (30,50,dejong_of,False)
        plotDejong()
    elif "r" in userRequest:
        of = (64,50,rosen_of, False)
        plotRosen()
    elif "h" in userRequest:
        of = (48,50,himmel_of, False)
    elif "f" in userRequest:
        userRequest = input("How many values? (10 - 27): ")
        line = (int(userRequest) - 10) * 2
        print(line)
        file = open("given_of.txt", "r")
        file.seek(0)
        i = 0
        while i < line:
            file.readline()
            i+=1
        Lines.append(file.readline())
        Lines.append(file.readline()[:-2])
        of = (int(userRequest), 50, dynamic_of, False)
    return of
