


class Device:
    _source_device_id = None
    _source_subnet_id = None
    _source_device_type_hex = None
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
        self._operate_code_hex = operate_code_hex
        self._target_subnet_id = target_subnet_id
        self._target_device_id = target_device_id
        self._content = content


        
        
        

def decode_message(message):
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



    
    
device = decode_message(b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0f\x01\x17\x00\x95\x001\x01J\x01d\x00\x03\xd7\xd1')

c = ''
for byte in device.content:
    c += str(byte) + ' '

print(f"{device.source_subnet_id}.{device.source_device_id} -> {device.target_subnet_id}.{device.target_device_id} [{c}]")
