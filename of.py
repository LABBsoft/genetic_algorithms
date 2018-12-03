import struct
import multiprocessing
from charts import *

Lines = []

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

def rosen_of(s):
    x = bitToFloat(s[:32])[0]
    y = bitToFloat(s[32:])[0]
    ans = abs(100 * pow(y - pow(x,2),2) + pow(x-1, 2))
    return ans

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
    return eval(Lines[1])

# Use string size divisible by 10
# Max value 
def dejong_of(s):
    fitness = 0
    for i, c in enumerate(s):
        if i % 10 == 0:
            if i != 0:
                cur /= 100
                fitness += cur * cur
            cur = -512
        if c == '1':
            cur += 2 ** (i % 10)
    cur /= 100
    fitness += cur * cur
    return fitness

def useWhich():
    of = (0,0,None,True)
    userRequest = input("""Use which Objective Function?
dejong: d 
rosenbrock: r 
from file: f
-> """)
    if "d" in userRequest:
        of = (30,50,dejong_of,False)
    elif "r" in userRequest:
        of = (64,50,rosen_of, False)
        p = multiprocessing.Process(target=plotRosen, args=())
        p.start()
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
