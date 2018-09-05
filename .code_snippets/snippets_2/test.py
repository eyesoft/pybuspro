import struct

b = b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0f\x01\x17\x00\x95\x001\x01J\x01d\x00\x03\xd7\xd1'
r = ''

for s in b:
    r += str(s) + ' '

print(b)
print(r)


#n = bytes.fromhex("ab be")

#print(n)
