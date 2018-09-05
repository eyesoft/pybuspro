#pip install crc16==0.1.1

import asyncio
import socket
import sys

from pybuspro.api.telegram import Telegram
from pybuspro.api.enums import DeviceType
from crc16 import *
import binascii
from struct import *

# ip, port = gateway_address
# subnet_id, device_id, channel = device_address


class Buspro:

    def __init__(self, gateway_address):
        self._telegram_received_cbs = []
        self._gateway_address = gateway_address
        self._socket = None
        
    def register_telegram_received_cb(self, telegram_received_cb, device_address):
        self._telegram_received_cbs.append({'callback':telegram_received_cb, 'device_address':device_address})

    async def disconnect(self):
        self._socket.close()

    async def connect(self):
        try:
            print('Creating socket...')
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print('Socket created')
        except socket.error as msg:
            print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        # Bind socket to local host and port
        try:
            port = self._gateway_address[1]
            print(f'Binding to port {port}...')
            s.bind(('', port))
            print(f'Socket bind to port {port} complete')
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        self._socket = s

    async def send_message(self, telegram: Telegram):
        await asyncio.sleep(0.1)
        print(f"send telegram: {telegram}...")

    async def start_listen(self, callback=None):
        await self.full(callback)
        # await self.simple(callback)

    async def simple(self, callback=None):
        iterations = 15
        i = 0
        while True:
            i += 1

            telegram = Telegram(source_address=(1, 120, 10))
            telegram.payload = f"[{i}]"
            # print(telegram.payload)
            # print(telegram.source_address)
            # print(str(telegram))

            if callback is not None:
                await callback(telegram)

            for telegram_received_cb in self._telegram_received_cbs:
                device_address = telegram_received_cb['device_address']

                # Sender callback kun for oppgitt kanal
                if device_address[2] == i:
                    ret = await telegram_received_cb['callback'](f"{device_address} ==> {str(telegram)}")

            if i == iterations:
                break

            await asyncio.sleep(1)

    async def full(self, callback=None):

        if not self._socket:
            print('Socket not created. Please run connect().')
            sys.exit()

        # now keep talking with the client
        while 1:
            # receive data from client (data, addr)
            # data, udp_address = self._socket.recvfrom(1024)

            udp_address = ('192.168.1.15', 6000)
            data = b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0f\x01\x17\x00\x95\x001\x01J\x01d\x00\x03\xd7\xd1'

            if not data:
                break

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

            crc_check_pass = self.check_crc(data)
            # crc_check_pass = False
            if not crc_check_pass:
                print("CRC check of received data failed")
                continue

            telegram = Telegram()
            telegram.source_device_type = source_device_type_hex
            telegram.raw_data = data
            telegram.source_address = (source_subnet_id, source_device_id)
            telegram.operate_code = operate_code_hex
            telegram.target_address = (target_subnet_id, target_device_id)
            telegram.udp_address = udp_address
            telegram.payload = content

            print(f"_Data: {self.hex_to_integer(data)}")
            print(f"_DeviceType: {DeviceType(source_device_type_hex)}")     # Returns DeviceType
            print(f"_SendBuf: {self.build_buf_to_send(telegram)}")

            if callback:
                await callback(f"Received telegram from callback: {telegram}")

            '''
            for telegram_received_cb in self._telegram_received_cbs:
                device_address = telegram_received_cb['device_address']

                # Sender callback kun for oppgitt kanal
                if device_address[2] == i:
                    await telegram_received_cb['callback'](f"{device_address} ==> {str(telegram)}")
            '''

            break

        await self.disconnect()

    @staticmethod
    def build_buf_to_send(telegram: Telegram):

        send_buf = bytearray([192, 168, 1, 15])
        send_buf.extend('HDLMIRACLE'.encode())
        send_buf.append(0xAA)
        send_buf.append(0xAA)

        length_of_data_package = 11 + len(telegram.payload)
        send_buf.append(length_of_data_package)

        sender_subnet_id, sender_device_id = telegram.source_address
        send_buf.append(sender_subnet_id)
        send_buf.append(sender_device_id)

        send_buf.append(telegram.source_device_type[0])
        send_buf.append(telegram.source_device_type[1])

        send_buf.append(telegram.operate_code[0])
        send_buf.append(telegram.operate_code[1])

        target_subnet_id, target_device_id = telegram.target_address
        send_buf.append(target_subnet_id)
        send_buf.append(target_device_id)

        for byte in telegram.payload:
            send_buf.append(byte)

        crc_buf_length = length_of_data_package - 2
        crc_buf = send_buf[-crc_buf_length:]
        crc_buf_as_bytes = bytes(crc_buf)
        crc = crc16xmodem(crc_buf_as_bytes)
        hex_byte_array = pack(">H", crc)

        send_buf.append(hex_byte_array[0])
        send_buf.append(hex_byte_array[1])

        return send_buf

    @staticmethod
    def check_crc(data):
        crc = b'\xd7\xd1'
        return True

    @staticmethod
    def hex_to_integer(hex_value):
        list_of_integer = []
        for string in hex_value:
            list_of_integer.append(string)
        return list_of_integer

