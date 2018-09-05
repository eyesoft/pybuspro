#pip install crc16==0.1.1
#pip install crcmod


#import binascii
from struct import *
from crc16 import *
#import crcmod

#import binascii



     

    
    
#crc = crc('dette er en tekst')
#crc = crcb(b'\x0f\x01\x17\x00\x95\x001\x01J\x01d\x00\x03')

#lengthOfDataPackage=15
#crcBufLength = 13


data = b'\x0f\x01\x17\x00\x95\x001\x01J\x01d\x00\x03'

crc = crc16xmodem(data)

hex_byte_array = pack(">H", crc)

print(hex_byte_array)


# # r t in data:
    # # int(t)

# # int("")

#crc = crc16(data)
#crc = crcb(0x31,0x32,0x33)

# # int("")



#print('{:04x}'.format(crc))
#print(crc)
#print(pack(">I", 4003).encode('hex'))

#print(pack('hhl', 1, 2, 3))
#print(pack('hhl', 1, 2, 3))

# for s in crc:
    # print(s)

#\xd7\xd1