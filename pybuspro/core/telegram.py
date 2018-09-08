import json

from .enums import DeviceType, OperateCode
from crc16 import *
from struct import *


# DTO class
class Telegram:
    def __init__(self):
        self.udp_address = None

        self.payload = None
        # self.payload_list = None

        # self.operate_code_hex = None
        self.operate_code = None

        # self.source_device_type_hex = None
        self.source_device_type = None

        self.udp_data = None
        # self.raw_data_list = None

        self.source_address = None
        self.target_address = None

        self.crc = None

    def __str__(self):
        """Return object as readable string."""

        return json.JSONEncoder().encode([
            {"name": "source_address", "value": self.source_address},
            # {"name": "source_device_type_hex", "value": str(self.source_device_type_hex)},
            {"name": "source_device_type", "value": str(self.source_device_type)},
            {"name": "target_address", "value": self.target_address},
            # {"name": "operate_code_hex", "value": str(self.operate_code_hex)},
            {"name": "operate_code", "value": str(self.operate_code)},
            {"name": "payload", "value": str(self.payload)},
            # {"name": "payload_list", "value": str(self.payload_list)},
            {"name": "udp_address", "value": self.udp_address},
            {"name": "udp_data", "value": str(self.udp_data)},
            # {"name": "raw_data_list", "value": str(self.raw_data_list)},
            # {"name": "raw_data", "value": str(self.raw_data)},
            {"name": "crc", "value": str(self.crc)},
        ])

    def __eq__(self, other):
        """Equal operator."""
        return self.__dict__ == other.__dict__


class TelegramHelper:

    def build_telegram(self, data, address):
        if not data:
            return None

        # print(data)

        index_length_of_data_package = 16
        index_original_subnet_id = 17
        index_original_device_id = 18
        index_original_device_type = 19
        index_operate_code = 21
        index_target_subnet_id = 23
        index_target_device_id = 24
        index_content = 25
        length_of_data_package = data[index_length_of_data_package]

        source_device_id = data[index_original_device_id]
        content_length = length_of_data_package - 1 - 1 - 1 - 2 - 2 - 1 - 1 - 1 - 1
        source_subnet_id = data[index_original_subnet_id]
        source_device_type_hex = data[index_original_device_type:index_original_device_type + 2]
        operate_code_hex = data[index_operate_code:index_operate_code + 2]
        target_subnet_id = data[index_target_subnet_id]
        target_device_id = data[index_target_device_id]
        content = data[index_content:index_content + content_length]
        crc = data[-2:]

        telegram = Telegram()
        # telegram.source_device_type_hex = source_device_type_hex
        telegram.source_device_type = self._get_enum_value(DeviceType, source_device_type_hex)
        telegram.udp_data = data
        # telegram.raw_data_list = self._hex_to_integer_as_list(data)
        telegram.source_address = (source_subnet_id, source_device_id)
        # telegram.operate_code_hex = operate_code_hex
        telegram.operate_code = self._get_enum_value(OperateCode, operate_code_hex)
        telegram.target_address = (target_subnet_id, target_device_id)
        telegram.udp_address = address
        # telegram.payload = content
        telegram.payload = self._hex_to_integer_list(content)
        telegram.crc = crc

        crc_check_pass = self._check_crc(telegram)
        if not crc_check_pass:
            print("ERROR: CRC check of received data failed")
            return None

        # print(crc)
        # print(self._calculate_crc(telegram))
        # print(f"LOG: Data: {self.hex_to_integer(data)}")
        # print(f"LOG: DeviceType: {DeviceType(source_device_type_hex)}")  # Returns DeviceType
        # print(f"LOG: SendBuf: {self.build_send_buffer(telegram)}")

        return telegram

    def build_send_buffer(self, telegram: Telegram):
        send_buf = bytearray([192, 168, 1, 15])
        send_buf.extend('HDLMIRACLE'.encode())
        send_buf.append(0xAA)
        send_buf.append(0xAA)

        length_of_data_package = 11 + len(telegram.payload)
        send_buf.append(length_of_data_package)

        if telegram.source_address is not None:
            sender_subnet_id, sender_device_id = telegram.source_address
        else:
            sender_subnet_id = 200
            sender_device_id = 200

        send_buf.append(sender_subnet_id)
        send_buf.append(sender_device_id)

        if telegram.source_device_type is not None:
            source_device_type_hex = telegram.source_device_type.value
            send_buf.append(source_device_type_hex[0])
            send_buf.append(source_device_type_hex[1])
        else:
            send_buf.append(0)
            send_buf.append(0)

        # if telegram.source_device_type_hex is not None:
        #    send_buf.append(telegram.source_device_type_hex[0])
        #    send_buf.append(telegram.source_device_type_hex[1])
        # else:
        #     send_buf.append(0)
        #    send_buf.append(0)
        #    # send_buf.append(b'\x00\x00')

        operate_code_hex = telegram.operate_code.value
        send_buf.append(operate_code_hex[0])
        send_buf.append(operate_code_hex[1])

        target_subnet_id, target_device_id = telegram.target_address
        send_buf.append(target_subnet_id)
        send_buf.append(target_device_id)

        for byte in telegram.payload:
            send_buf.append(byte)

        # crc_buf_length = length_of_data_package - 2
        # crc_buf = send_buf[-crc_buf_length:]
        # crc_buf_as_bytes = bytes(crc_buf)
        # crc = crc16xmodem(crc_buf_as_bytes)
        # hex_byte_array = pack(">H", crc)
        # send_buf.append(hex_byte_array[0])
        # send_buf.append(hex_byte_array[1])

        crc_0, crc_1 = self._calculate_crc(length_of_data_package, send_buf)
        send_buf.append(crc_0)
        send_buf.append(crc_1)

        return send_buf

    @staticmethod
    def _calculate_crc(length_of_data_package, send_buf):
        crc_buf_length = length_of_data_package - 2
        crc_buf = send_buf[-crc_buf_length:]
        crc_buf_as_bytes = bytes(crc_buf)
        crc = crc16xmodem(crc_buf_as_bytes)
        return pack(">H", crc)

    @staticmethod
    def _calculate_crc_from_telegram(telegram):
        length_of_data_package = 11 + len(telegram.payload)
        crc_buf_length = length_of_data_package - 2
        send_buf = telegram.udp_data[:-2]
        crc_buf = send_buf[-crc_buf_length:]
        crc_buf_as_bytes = bytes(crc_buf)
        crc = crc16xmodem(crc_buf_as_bytes)
        return pack(">H", crc)

    def _check_crc(self, telegram):
        # crc = data[-2:]
        calculated_crc = self._calculate_crc_from_telegram(telegram)
        if calculated_crc == telegram.crc:
            return True
        return False

    @staticmethod
    def _hex_to_integer_list(hex_value):
        list_of_integer = []
        for string in hex_value:
            list_of_integer.append(string)
        return list_of_integer

    @staticmethod
    def _enum_has_value(enum, value):
        return any(value == item.value for item in enum)

    def _get_enum_value(self, enum, value):
        if enum == DeviceType:
            if self._enum_has_value(enum, value):
                return DeviceType(value)
            else:
                return None
        elif enum == OperateCode:
            if self._enum_has_value(enum, value):
                return OperateCode(value)
            else:
                return None

