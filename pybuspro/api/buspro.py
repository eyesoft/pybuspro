import asyncio
import socket
import sys

from pybuspro.api.telegram import Telegram

# ip, port = gateway_address
# subnet_id, device_id, channel = device_address

class Buspro():

    def __init__(self, gateway_address):
        self._telegram_received_cbs = []
        self._gateway_address = gateway_address
        
    def register_telegram_received_cb(self, telegram_received_cb, device_address):
        self._telegram_received_cbs.append({'callback':telegram_received_cb, 'device_address':device_address})

    async def connect(self):
        print(f"...Connected to {self._gateway_address}...")
        
    async def _send_message(self, telegram):
        await asyncio.sleep(0.1)
        print(f"send telegram: {telegram}...")

    async def start(self, callback=None):

        '''
        # Datagram (udp) socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print('Socket created')
        except socket.error as msg:
            print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        # Bind socket to local host and port
        try:
            port = self._gateway_address[1]
            s.bind(('', port))
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        print('Socket bind complete')

        # now keep talking with the client
        while 1:

            # receive data from client (data, addr)
            data, addr = s.recvfrom(1024)
            # data = d[0]
            # addr = d[1]

            addr0 = str(addr[0])
            addr1 = str(addr[1])

            if not data:
                break

            r = ''
            for ss in data:
                r += str(ss) + ' '


            telegram = Telegram(source_address=(1,120,10))
            telegram.payload = data
            #print(telegram.payload)
            #print(telegram.source_address)
            #print(str(telegram))




            if callback:
                await callback(telegram)




            for telegram_received_cb in self._telegram_received_cbs:
               device_address = telegram_received_cb['device_address']

            a=""
            # Sender callback kun for oppgitt kanal
#            if device_address[2] == i:
#                ret = await telegram_received_cb['callback'](f"{device_address} ==> {str(telegram)}")

        s.close()
        '''

        iterations = 15
        i = 0
        while True:
             i += 1

             telegram = Telegram(source_address=(1,120,10))
             telegram.payload = f"[{i}]"
             #print(telegram.payload)
             #print(telegram.source_address)
             #print(str(telegram))

             if callback is not None:
                 await callback(telegram)

             for telegram_received_cb in self._telegram_received_cbs:
                 device_address = telegram_received_cb['device_address']

                 # Sender callback kun for oppgitt kanal
                 if device_address[2] == i:
                     ret = await telegram_received_cb['callback'](f"{device_address} ==> {str(telegram)}")

             if i == iterations:
                 break;
             await asyncio.sleep(1)

