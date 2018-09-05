import asyncio

class EchoClientProtocol:
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print('Send:', self.message)
        #self.transport.sendto(self.message.encode())

    def datagram_received(self, data, addr):
        print('Received:', data.decode())

async def sendChar(transport, msg):
    print('send: ', msg)
    #transport.sendto(msg.encode())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    message = 'Hello World!'
    connect = loop.create_datagram_endpoint(
            lambda: EchoClientProtocol(message, loop),
            remote_addr=('192.168.1.159', 6000)
            )
    transport, protocol = loop.run_until_complete(connect)
    while (True):
        try:
            ch = input()
        except KeyboardInterrupt:
            break
        loop.run_until_complete(sendChar(transport, ch))
    loop.run_forever()
    transport.close()
    loop.close()