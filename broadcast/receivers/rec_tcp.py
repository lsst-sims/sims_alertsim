#!/usr/bin/env python

import socket


TCP_IP = '147.91.240.26'
TCP_PORT = 8098
BUFFER_SIZE = 16384  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(2)
#s.setblocking(0)

while 1:
    conn, addr = s.accept()
    print 'Connection address:', addr
#while 1:

    d1=conn.recv(4)
    print d1
    d2=d1.encode('hex')
    print 'duzina', d2 , int(d2,16)
    print 
    data = conn.recv(2*int(d2,16) )
#    if not data: break
    print len(data), int(d2,16)
    if len(data)==int(d2,16):
        print "received data:", data
    conn.send(str(len(data)))  # echo
    conn.close()
