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
    print 'Accepted connection from:', addr[0], ',', addr[1]
#while 1:

    d1=conn.recv(4)
    print 'Received hex:', d1
    d2=d1.encode('hex')
    print 'Received encoded:', d2
    print 'Length of', d2 , ':' , int(d2,16)
    # print 
    data = conn.recv(2*int(d2,16) )
#    if not data: break
    print 'Length of received data:' , len(data) # was: print len(data), int(d2,16)
    if len(data)==int(d2,16):
        print "Lengths are equal. Received data below:"
        print data
    else: print "Not equal"
    conn.send(str(len(data)))  # echo, back to sender
    # conn.send(str(addr[1])) # echo, back to sender
    conn.close()
    print '---------------------------------'
