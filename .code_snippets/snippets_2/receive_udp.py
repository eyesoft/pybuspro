
'''
slår på og av lys på kino
neste blir å starte lytting som egen tråd med callback
få inn async
'''


import socket
import sys
import time
 
HOST = '192.168.1.15'   # Symbolic name meaning all available interfaces
PORT = 6000 # Arbitrary non-privileged port


def callback(addr0, addr1, r, data):
    print('Message[' + addr0 + ':' + addr1 + '] - ' + r)
    print('Message[' + addr0 + ':' + addr1 + '] - ' + str(data))
    print('')

def main(callback=None):

    # Datagram (udp) socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('Socket created')
    except socket.error as msg:
        print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
     
     
    # Bind socket to local host and port
    try:
        s.bind(('', PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
         
    print('Socket bind complete')

    lys_paa_kino = b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0f\x01\x17\x00\x95\x001\x01J\x01d\x00\x03\xd7\xd1'
    #s.sendto(lys_paa_kino, (HOST, PORT))

    #time.sleep(5)

    lys_av_kino = b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0f\x01\x17\x00\x95\x001\x01J\x01\x00\x00\x03\x90z'
    #s.sendto(lys_av_kino, (HOST, PORT))


    #now keep talking with the client
    while 1:


        # receive data from client (data, addr)
        data, addr = s.recvfrom(1024)
        #data = d[0]
        #addr = d[1]

        addr0 = str(addr[0])
        addr1 = str(addr[1])
         
        if not data: 
            break

        r = ''
        for ss in data:
            r += str(ss) + ' '

        if callback:
            callback(addr0, addr1, r, data)

         
    s.close()



main(callback)
#main()
