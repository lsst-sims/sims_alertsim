import socket
import struct
import sys
import errno
import zlib

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

    def close_and_exist(self):
        self.close()
        sys.exit(1)

    #@staticmethod
    def _add_voevent_header(self, message):
        header = '%08x' % (len(message))
        return header.decode('hex') + message

class TcpIp(Broadcast):

    '''
    class for TcpIp broadcast
    '''

    def __init__(self, ip, port, header):
        self.header = header
        self.ip = ip
        self.port = port
        try:
            self._connect_socket()
        except socket.error as e:
            print(e)
            self.close_and_exit()

    def send(self, message):
        #message = zlib.compress(message, 9)
        #message += "\nEOF\n"
        print message
        try:
            self._send_and_receive(message)
        except socket.error as e:
            if e.errno == errno.EPIPE:
                self._connect_socket()
                self._send_and_receive(message)
            else: 
                print(e)
                self.close_and_exit()
    
    def _connect_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))
        print "Connected to %s at port %d" % (self.ip, self.port)

    def _send_and_receive(self, message):
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
            self.close_and_exit()

