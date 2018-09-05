import socket   #for sockets
import sys  #for exit
 
# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 6000 # Arbitrary non-privileged port

s.bind((HOST, PORT))

#while(1) :
#msg = input('Enter message to send : ')
 
try :
    #Set the whole string

    msg = b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0f\x01\x17\x00\x95\x001\x01J\x01d\x00\x03\xd7\xd1'

    s.sendto(msg, (HOST, PORT))

    print(msg)
    # receive data from client (data, addr)
    #d = s.recvfrom(1024)
    #reply = d[0]
    #addr = d[1]
     
    #print('Server reply : ' + reply)
 
except socket.error as msg:
    print('Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()