import socket
import struct
import sys

class Broadcast(object):

    '''
    abstract base class, with common broadcast functionalities (expecting more to come)
    '''

    BUFFER_SIZE = 10000

    def __init__(self):
        pass

    def send(self, message):
        pass

    def close(self):
        self.sock.close()
        print >>sys.stderr, 'closing socket'
        sys.exit(1)
    
    @staticmethod
    def _add_voevent_header(message):
        header = '%08x' % (len(message))
        return header.decode('hex') + message

class TcpIp(Broadcast):

    '''
    class for TcpIp broadcast
    '''

    def __init__(self, ip, port, header):
        self.header = header
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((ip, port))
            print "Connected to %s at port %d" % (ip, port)
        except socket.error as e:
            print(e)
            self.close()

    def send(self, message):
        self.sock.send(self._add_voevent_header(message)) if self.header else self.sock.send(message) 
        data = self.sock.recv(self.BUFFER_SIZE)
        print "received data:", data

class Multicast(Broadcast):
    
    '''
    class for multicast // to be revised
    '''

    def __init__(self, ip, port):
        self.multicast_group = (ip, 5032)

        # Create the datagram socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set a timeout so the socket does not block indefinitely when trying
        # to receive data.
        self.sock.settimeout(1)

        # Set the time-to-live for messages to 1 so they do not go past the
        # local network segment.
        ttl = struct.pack('b', -128)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)


    def send(self, message):

        try:

            # Send data to the multicast group
            print >>sys.stderr, 'sending "%s"' % message
            sent = self.sock.sendto(message, multicast_group)

            # Look for responses from all recipients
            while True:
                print >>sys.stderr, 'waiting to receive'
                try:
                    data, server = self.sock.recvfrom(16)
                except socket.timeout:
                    print >>sys.stderr, 'timed out, no more responses'
                    break
                else:
                    print >>sys.stderr, 'received "%s" from %s' % (data, server)

        finally:
            print >>sys.stderr, 'closing socket'
            self.close()

