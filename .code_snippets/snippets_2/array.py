#pip install crc16==0.1.1
from struct import *
from crc16 import *
import binascii






def decode_message(message):
    # print("decode: ")
    # print(message)

    raw_data = message
    
    indexLengthOfDataPackage = 16
    indexOriginalSubnetId = 17
    indexOriginalDeviceId = 18
    indexOriginalDeviceType = 19
    indexOperateCode = 21
    indexTargetSubnetId = 23
    indexTargetDeviceId = 24
    indexContent = 25
    lengthOfDataPackage = message[indexLengthOfDataPackage]

    source_device_id = message[indexOriginalDeviceId]
    
    ContentLength = lengthOfDataPackage - 1 - 1 - 1 - 2 - 2 - 1 - 1 - 1 - 1
    SourceSubnetId = message[indexOriginalSubnetId]
    SourceDeviceTypeHex = message[indexOriginalDeviceType:indexOriginalDeviceType+2]
    OperateCodeHex = message[indexOperateCode:indexOperateCode+2]
    TargetSubnetId = message[indexTargetSubnetId]
    TargetDeviceId = message[indexTargetDeviceId]
    content = message[indexContent:indexContent+ContentLength]
    
    c = ''
    for byte in content:
        c += str(byte) + ' '
    
    print(f"SourceSubnetId = {SourceSubnetId}")
    print(f"source_device_id = {source_device_id}")
    print(f"SourceDeviceTypeHex = {SourceDeviceTypeHex} ({SourceDeviceTypeHex[0]} {SourceDeviceTypeHex[1]})")

    print(f"TargetSubnetId = {TargetSubnetId}")
    print(f"TargetDeviceId = {TargetDeviceId}")
    
    print(f"ContentLength = {ContentLength}")
    print(f"OperateCodeHex = {OperateCodeHex} ({OperateCodeHex[0]} {OperateCodeHex[1]})")

    print(f"content = {content} ({c})")
    
    
    
    
    
decode_message(b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0f\x01\x17\x00\x95\x001\x01J\x01d\x00\x03\xd7\xd1')



















def build_buf_to_send(target_subnet_id, target_device_id, operate_code, content, sender_subnet_id, sender_device_id, sender_device_type):
    #print("build")
    
    #length = 25 + len(content) + 2
    #print(length)

    ###############################################
    # Konvertere chat til hex og tilbake
    #hex = binascii.hexlify(b'c')
    #print(hex)                         # b'63'
    #print(str(hex, 'ascii'))           # 63
    
    #print("")
    
    #string = binascii.unhexlify(hex)
    #print(string)                      # b'c'    
    #print(str(string, 'ascii'))        # c    
    ###############################################

   
    send_buf = bytearray([192, 168, 1, 15])
    #send_buf.append(binascii.hexlify(b'H'))
    #send_buf.append(b'1')
    #send_buf.append(0x04)
    #send_buf.append(4)
    #send_buf.append(int(binascii.hexlify(b'H')))
    send_buf.extend('HDLMIRACLE'.encode())
    send_buf.append(0xAA)
    send_buf.append(0xAA)
    
    length_of_data_package = 11 + len(content)
    #length_of_data_package = 15
    
    send_buf.append(length_of_data_package)
    
    send_buf.append(sender_subnet_id)
    send_buf.append(sender_device_id)

    send_buf.append(sender_device_type[0])
    send_buf.append(sender_device_type[1])
    
    send_buf.append(operate_code[0])
    send_buf.append(operate_code[1])
    
    send_buf.append(target_subnet_id)
    send_buf.append(target_device_id)
    
    for byte in content:
        send_buf.append(byte)
    
    ################
    # CRC
    #print(send_buf)
    
    length = length_of_data_package - 2
    crc_buf = send_buf[-length:]
    #print(crc_buf)
    
    crc_buf_as_bytes = bytes(crc_buf)
    crc = crc16xmodem(crc_buf_as_bytes)
    hex_byte_array = pack(">H", crc)
    
    # print(hex_byte_array[0])
    # print(hex_byte_array[1])
    
    send_buf.append(hex_byte_array[0])
    send_buf.append(hex_byte_array[1])
    ################

  
    print(send_buf)
    
           
    #print(bytes(send_buf))
    
    #send_buf_as_bytearray = bytearray([0x13, 0x00, 0x00])
    #print(send_buf_as_bytearray)
    
    #send_buf_as_bytes = bytes(send_buf_as_bytearray)
    #print(send_buf_as_bytes)
    
    for s in send_buf:
        print(s)
        



        
    
# channel_no = 1
# intensity = 100
# running_time_minutes = 0
# running_time_seconds = 3
# content = bytearray([channel_no, intensity, running_time_minutes, running_time_seconds])
    
# target_subnet_id = 1
# target_device_id = 74
# operate_code = bytearray([0, 49])

# sender_subnet_id = 1
# sender_device_id = 23
# sender_device_type = bytearray([0, 149])
    
# build_buf_to_send(target_subnet_id, target_device_id, operate_code, content, sender_subnet_id, sender_device_id, sender_device_type)


    
# 192
# 168
# 1
# 15
# 72
# 68
# 76
# 77
# 73
# 82
# 65
# 67
# 76
# 69
# 170
# 170
# 15
# 1
# 23
# 0
# 149
# 0
# 49
# 1
# 74
# 1
# 100
# 0
# 3
# 215
# 209    
    

#lys_paa_kino = b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0f\x01\x17\x00\x95\x001\x01J\x01d\x00\x03\xd7\xd1'


#b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0f\x01\x17\x00\x95\x001\x01J\x01d\x00\x03\xd7\xd1'
#b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0f\x01\x17\x00\x95\x001\x01J\x01d\x00\x03\xd7\xd1'
#b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0f\x01\x17\x00\x95\x001\x01J\x01d\x00\x03\xd7\xd1'
#print(lys_paa_kino[0])


#for s in lys_paa_kino:
#    print(s)
    
    









