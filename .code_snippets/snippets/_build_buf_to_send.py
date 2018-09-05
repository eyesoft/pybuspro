#pip install crc16==0.1.1
from struct import *
from crc16 import *
import binascii

def build_buf_to_send(target_subnet_id, target_device_id, operate_code, content, sender_subnet_id, sender_device_id, sender_device_type):
   
    send_buf = bytearray([192, 168, 1, 15])
    send_buf.extend('HDLMIRACLE'.encode())
    send_buf.append(0xAA)
    send_buf.append(0xAA)
    
    length_of_data_package = 11 + len(content)
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
    
    crc_buf_length = length_of_data_package - 2
    crc_buf = send_buf[-crc_buf_length:]
    crc_buf_as_bytes = bytes(crc_buf)
    crc = crc16xmodem(crc_buf_as_bytes)
    hex_byte_array = pack(">H", crc)
    
    send_buf.append(hex_byte_array[0])
    send_buf.append(hex_byte_array[1])
  
    return send_buf






channel_no = 1
intensity = 100
running_time_minutes = 0
running_time_seconds = 3
content = bytearray([channel_no, intensity, running_time_minutes, running_time_seconds])
    
target_subnet_id = 1
target_device_id = 74
operate_code = bytearray([0, 49])

sender_subnet_id = 1
sender_device_id = 23
sender_device_type = bytearray([0, 149])
    
buf = build_buf_to_send(target_subnet_id, target_device_id, operate_code, content, sender_subnet_id, sender_device_id, sender_device_type)

print('')
print("Bytearray representation:")
print(buf)
print('')
print("Integer representation:")
    
s = ''
for i in buf:
    s += str(i) + ' '
    
print(s)