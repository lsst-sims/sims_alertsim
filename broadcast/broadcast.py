import socket
import struct
import sys, time

class Broadcast(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def send(self, message):
        pass

class TcpIp(Broadcast):

    def send(self, message):

        TCP_IP = self.ip
        TCP_PORT = self.port
        BUFFER_SIZE = 10000
        MESSAGE = message
        """
        #print len(message)
        #print hex(len(message)+32)
        #msg1=hex(len(message))
        #print len(msg1)
        msg1=''
        #if xzz==0:
        msg1= '%08x'% (len(message))
        msg1=msg1.decode('hex')
        cv= '%08x'% 22
        cv=cv.decode('hex')
        eot='%08x'% 4
        eot=eot.decode('hex')
        #print msg1
        #print eot.decode('hex')
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((TCP_IP, TCP_PORT))
        #s.bind((TCP_IP, TCP_PORT))
        #s.send('2')
        msg1= '%08x'% (len(message))
        msg1=msg1.decode('hex')
                 
        s.send(msg1)
        #print MESSAGE
        
        ww=s.send(MESSAGE)
        print ww,  'Message size:', len(MESSAGE)
        eot='%08x'% 4
        eot=eot.decode('hex')
        #s.send(eot)
         
        data = s.recv(BUFFER_SIZE)
        print int(data)
        counter=0
        time1=time.clock()
        while int(data) != ww:
            counter=counter+1
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((TCP_IP, TCP_PORT))
            s.send(msg1)
            ww1=s.send(MESSAGE)
            data = s.recv(BUFFER_SIZE)
            ww=ww1


        s.close()
        time2=time.clock()
        
        print "Number of retries:", counter
        print "Time duration:", time2-time1
        print "Received data (echo from receiver):", data
        print "---------------------------"

class Multicast(Broadcast):

    def send(self, message):

        multicast_group = (self.ip, 5032)

        # Create the datagram socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set a timeout so the socket does not block indefinitely when trying
        # to receive data.
        sock.settimeout(1)

        # Set the time-to-live for messages to 1 so they do not go past the
        # local network segment.
        ttl = struct.pack('b', -128)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        try:

            # Send data to the multicast group
            print >>sys.stderr, 'sending "%s"' % message
            sent = sock.sendto(message, multicast_group)

            # Look for responses from all recipients
            while True:
                print >>sys.stderr, 'waiting to receive'
                try:
                    data, server = sock.recvfrom(16)
                except socket.timeout:
                    print >>sys.stderr, 'timed out, no more responses'
                    break
                else:
                    print >>sys.stderr, 'received "%s" from %s' % (data, server)

        finally:
            print >>sys.stderr, 'closing socket'
            sock.close()

