import struct
import random
def bitToFloat(bits):
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
    print(byte)
    f = struct.unpack('f',bytes(byte))
    return f

bits = []
for i in range(32):
    bits.append(str(random.randint(0,1)))
f = bitToFloat(bits)
print(f)