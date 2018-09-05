from enum import Enum  
import socket
import sys
import time
import datetime
 


class Device:
    _source_device_id = None
    _source_subnet_id = None
    _source_device_type_hex = None
    _source_device_type = None
    _operate_code_hex = None
    _target_subnet_id = None
    _target_device_id = None
    _content = None
    
    @property
    def source_device_id(self):
        return self._source_device_id

    @property
    def source_subnet_id(self):
        return self._source_subnet_id

    @property
    def source_device_type_hex(self):
        return self._source_device_type_hex

    @property
    def source_device_type(self):
        return self._source_device_type

    @property
    def operate_code_hex(self):
        return self._operate_code_hex

    @property
    def target_subnet_id(self):
        return self._target_subnet_id

    @property
    def target_device_id(self):
        return self._target_device_id

    @property
    def content(self):
        return self._content
        
    def __init__(self, source_device_id, source_subnet_id, source_device_type_hex, operate_code_hex, target_subnet_id, target_device_id, content):
        self._source_device_id = source_device_id
        self._source_subnet_id = source_subnet_id
        self._source_device_type_hex = source_device_type_hex
        
        devicetype = ''
        try:
            devicetype = DeviceType(source_device_type_hex)
        except:
            devicetype = '<Unknown>'
        self._source_device_type = devicetype
        
        self._operate_code_hex = operate_code_hex
        self._target_subnet_id = target_subnet_id
        self._target_device_id = target_device_id
        self._content = content

        
class DeviceType(Enum):
    NotSet = 0x0
    SB_DN_6B0_10v = b'\x00\x11' # Rele varme
    SB_DN_SEC250K = b'\x0B\xE9'	# Sikkerhetsmodul
    SB_CMS_12in1 = b'\x01\x34'  # 12i1
    SB_DN_Logic960 = b'\x04\x53'# Logikkmodul
    SB_DLP2 = b'\x00\x86'		# DLP
    SB_DLP = b'\x00\x95'		# DLP
    SB_DLP_v2 = b'\x00\x9C'			# DLPv2
    SmartHDLTest = b'\xFF\xFD'
    SetupTool = b'\FF\xFE'
    SB_WS8M = b'\x01\x2B'			# 8 keys panel
    SB_CMS_8in1 = b'\x01\x35'		# 8i1
    SB_DN_DT0601 = b'\x02\x60'		# 6ch Dimmer
    SB_DN_R0816 = b'\x01\xAC'		# Rele
    #SB_DN_DT0601 = 0x009E	    # Universaldimmer 6ch 1A
    #SB_DN_RS232N				# RS232
    
    
class Buspro:
    _host = None
    _port = None
    
    def __init__(self, host, port):
        self._host = host
        self._port = port
        
    def decode_message(self, message):
        raw_data = message
        
        index_length_of_data_package = 16
        index_original_subnet_id = 17
        index_original_device_id = 18
        index_original_device_type = 19
        index_operate_code = 21
        index_target_subnet_id = 23
        index_target_device_id = 24
        index_content = 25
        length_of_data_package = message[index_length_of_data_package]

        source_device_id = message[index_original_device_id]
        
        content_length = length_of_data_package - 1 - 1 - 1 - 2 - 2 - 1 - 1 - 1 - 1
        source_subnet_id = message[index_original_subnet_id]
        source_device_type_hex = message[index_original_device_type:index_original_device_type + 2]
        operate_code_hex = message[index_operate_code:index_operate_code+2]
        target_subnet_id = message[index_target_subnet_id]
        target_device_id = message[index_target_device_id]
        content = message[index_content:index_content + content_length]

        device = Device(source_device_id, source_subnet_id, source_device_type_hex, operate_code_hex, target_subnet_id, target_device_id, content)
        return device
    
    def start_receiver(self, callback, filter_sender_address=None, filter_target_address=None):

        # Datagram (udp) socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print('Socket created')
        except socket.error as msg:
            print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()
         
        # Bind socket to local host and port
        try:
            s.bind(('', self._port))
            print(f'Socket bind complete on port {self._port}')
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        if filter_sender_address is not None:
            print(f"Viser kun meldinger fra {filter_sender_address}")

        if filter_target_address is not None:
            print(f"Viser kun meldinger til {filter_target_address}")
            
        print('')
            
        while 1:

            # receive data from client (data, addr)
            data, addr = s.recvfrom(1024)

            addr0 = str(addr[0])
            addr1 = str(addr[1])
             
            if not data: 
                break

            r = ''
            for ss in data:
                r += str(ss) + ' '

            device = self.decode_message(data)
            
            do_callback = False
                        
            if filter_sender_address is not None:
                device_addr = filter_sender_address.split('.')
                if int(device_addr[0]) == device.source_subnet_id and int(device_addr[1]) == device.source_device_id:
                    do_callback = True
                    
            if filter_target_address is not None:
                device_addr = filter_target_address.split('.')
                if int(device_addr[0]) == device.target_subnet_id and int(device_addr[1]) == device.target_device_id:
                    do_callback = True

            if filter_sender_address is None and filter_target_address is None:
                do_callback = True
            
            if do_callback:
                callback(device)

             
        s.close()


    
    
    
    
    
def callback_print_parsed_message(device):
    # print('Message[' + addr0 + ':' + addr1 + '] - ' + r)
    # print('Message[' + addr0 + ':' + addr1 + '] - ' + str(data))
    # print('')
    
    c = ''
    for byte in device.content:
        c += str(byte) + ' '

    print(f"{device.source_subnet_id}.{device.source_device_id} ({device.source_device_type}) -> {device.target_subnet_id}.{device.target_device_id} [{c}]")
       
    if device.source_device_type == DeviceType.SB_DN_Logic960:
        print(f"Tidspunkt = {device.content[2]}/{device.content[1]}/{device.content[0]} {device.content[3]}:{device.content[4]}:{device.content[5]}")
    

    
def main():    
    
    host = '192.168.1.15'
    port = 6000 
       
    buspro = Buspro(host, port)
    #buspro.start_receiver(callback_print_parsed_message, "1.100")
    #buspro.start_receiver(callback_print_parsed_message, "1.110")
    #buspro.start_receiver(callback_print_parsed_message, "1.130")
    #buspro.start_receiver(callback_print_parsed_message, filter_target_address="255.255")
    buspro.start_receiver(callback_print_parsed_message, "1.130", "255.255")
    #buspro.start_receiver(callback_print_parsed_message, "1.40")
    #buspro.start_receiver(callback_print_parsed_message)
    
    
    
    #buspro.start_receiver(callback_print_parsed_message, address_filters)
    #self.xknx.telegram_queue.register_telegram_received_cb(self.telegram_received_cb, address_filters)
    
    


main()

