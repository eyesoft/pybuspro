"""Main module."""

import asyncio
import logging
import socket
import select

from asyncio import IncompleteReadError
from enum import Enum

_LOGGER = logging.getLogger(__name__)

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
DEFAULT_TIMEOUT = 10
DEFAULT_BUFFER_SIZE = 1024


class ConnectionState(Enum):
    DISCONNECTED = 0
    CONNECTED = 1

    
    


def checksum(command):
    """Function to calculate checksum."""
    crc = 0x147A
    # for b in command:
        # # rotate (crc 1 bit left)
        # crc = ((crc << 1) & 0xFFFF) | (crc & 0x8000) >> 15
        # crc = crc ^ 0xFFFF
        # crc = (crc + (crc >> 8) + b) & 0xFFFF
    return crc

def verify_and_strip(resp):
    """Verify checksum and strip header and footer of received frame."""
    return resp

def generate_query(command):
    """Add header, checksum and footer to command data."""
    data = bytearray(command)
    # c = checksum(data)
    # data.append(c >> 8)
    # data.append(c & 0xFF)
    # data.replace(b'\xFE', b'\xFE\xF0')
    data = bytearray.fromhex("FEFE") + data + bytearray.fromhex("FE0D")
    return data

def print_hex(data):
    """Debugging method to print out frames in hex."""
    hex_msg = ""
    for c in data:
        hex_msg += "\\x" + format(c, "02x")
    print(hex_msg)
    
    

    
    
    

class Buspro:
    """Asynchronous interface to talk to Buspro bus."""

    def __init__(self, host, port, loop):
        """Init the Buspro object."""
        self._host = host
        self._port = port
        self._loop = loop
        self._callback_a = None
        self._callback_b = None
        self._callback_c = None
        self._state = ConnectionState.DISCONNECTED
        self._socket = None
        self._message_handlers = {}

        # Assign handler
        self._message_handlers[b'\x00'] = self._message_handler_a
        self._message_handlers[b'\x17'] = self._message_handler_b
        self._message_handlers[b'\x0A'] = lambda msg: self._message_handler_c(ConnectionState.CONNECTED, msg)
        print("__init__ done")
       
    def _message_handler_a(self, msg):
        print("Returning status: %s", msg)
        if self._callback_a:
            self._callback_a(msg)
        return msg
       
    def _message_handler_b(self, msg):
        print("Returning status: %s", msg)
        if self._callback_b:
            self._callback_b(msg)
        return msg
       
    def _message_handler_c(self, mode, msg):
        print("Alarm update, mode: %s", mode)
        print("Returning status: %s", msg)
        
        if self._state in [mode, ConnectionState.DISCONNECTED]:
            self._state = ConnectionState.CONNECTED
        else:
            self._state = ConnectionState.DISCONNECTED

        if self._callback_c:
            self._callback_c(self._state)

        return self._state
       
    async def async_connect(self):
        """Make a TCP connection to the alarm system."""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.settimeout(DEFAULT_TIMEOUT)
        
        try:
            self._socket.connect((UDP_IP_ADDRESS, UDP_PORT_NO))
        except socket.error as err:
            print("Unable to bind on port %s: %s", UDP_PORT_NO, err)
            return False
        
        #self._socket.listen(10)
        #conn, addr = s.accept()
        
        print("connect done")
        return True
       
    def close(self):
        """Stop monitoring and close connection."""
        if self._socket:
            # self._activeConnection.Close()
            self._socket = None
            self._state = ConnectionState.DISCONNECTED
            print("Closing...")
    
    async def async_custom_action(self, code):
        """Send command to disarm."""
        print("Alarm disarm, code: %s")
        
        while len(code) < 16:
            code += 'F'

        code_bytes = bytearray.fromhex(code)

        data = generate_query(b'\x84' + code_bytes + self._partition_bytes)

        await self._send_data(data)    
    
    async def async_start_listen(self, callback_a=None, callback_b=None, callback_c=None):
        """Start monitoring of the alarm status.

        Send command to Buspro to start sending updates. Read in a
        loop and call respective callbacks when received messages.
        """
        print("starting async_start_listen")
        
        self._callback_a = callback_a
        self._callback_b = callback_b
        self._callback_c = callback_c

        print("Starting async_start_listen loop")
        print("Iteration... ")
        
        while True:
            status = await self._listen_to_bus()
            print("Got status!")
                
        print("Closed, quit monitoring.")
    
    def _listen_to_bus(self):
        print("Wait...")

        self._state = ConnectionState.CONNECTED
        
        try:
            resp = self._read_data()
        except IncompleteReadError as e:
            print("Got exception: %s. Most likely the other side has disconnected!", e)
            
            self._socket = None
            self._state = ConnectionState.DISCONNECTED
            return self._state

        if not resp:
            print("Got empty response. We think it's disconnect.")
            self._socket = None
            self._state = ConnectionState.DISCONNECTED
            return self._state

        msg_id = resp[0:1]
        if msg_id in self._message_handlers:
            print("Calling handler for id: %s", msg_id)
            return self._message_handlers[msg_id](resp)
        else:
            print("Ignoring message: %s", msg_id)
            return None

    def _read_data(self):
        # listen for incoming udp packet

        print("starting _read_data")
        
        # readable, _, _ = select.select([self._socket], [], [], DEFAULT_TIMEOUT)
        # if not readable:
            # print("Timeout (%s second(s)) waiting for data on port %s.", DEFAULT_TIMEOUT, UDP_PORT_NO)
            # return

        #data, _ = self._socket.recvfrom(DEFAULT_BUFFER_SIZE)        
        data = self._socket.recv(DEFAULT_BUFFER_SIZE)

        print("-- Receiving data --")
        print_hex(data)
        print("-- ------------- --")
        return verify_and_strip(data)
        
    def _send_data(self, data):
        print("-- Sending data --")
        print_hex(data)
        print("-- ------------- --")
        print("Sent %d bytes", len(data))

        #await self._writer.write(data)
        #clientSock.sendto(data, (UDP_IP_ADDRESS, UDP_PORT_NO))

        try:
            self._socket.send(data.encode())
        except socket.error as err:
            print("Unable to send payload %r to %s on port %s: %s", data, UDP_IP_ADDRESS, UDP_PORT_NO, err)
            return






            
    
    
    
    
def demo(host, port):
    """Basic demo."""

    print("starting demo")
    
    loop = asyncio.get_event_loop()
    client = Buspro(host, port, loop)

    loop.run_until_complete(client.async_connect())
    ## loop.create_task(client.async_custom_action("3333"))
    loop.create_task(client.async_start_listen())

    loop.run_forever()
    loop.close()    
    
    
    
demo("127.0.0.1", 1000)