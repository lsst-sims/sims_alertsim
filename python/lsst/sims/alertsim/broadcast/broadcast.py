import socket
import struct
import sys
import errno
import zlib
from lsst.log import Log

broadcastLog = Log.getLogger("sims.alerisim.broadcast.broadcastLogger")

class Broadcast(object):

    """
    Abstract base class, with common broadcast functionalities 
    """

    BUFFER_SIZE = 10000

    def __init__(self):
        """ implemented in daughter classes """
        pass

    def send(self, message):
        """ implemented in daughter classes """
        pass

    def close(self):
        """ close socket """
        self.sock.close()
        # print >>sys.stderr, 'closing socket'
        broadcastLog.info("Socket closed.")

    def close_and_exit(self):
        """ close socket and exit with code 1 (there was an issue) """
        self.close()
        sys.exit(1)

    #@staticmethod
    def _add_voevent_header(self, message):
        """ add 4 byte hex header at the beginning of the message """
        header = '%08x' % (len(message))
        return header.decode('hex') + message

class TcpIp(Broadcast):

    """
    Class for TcpIp broadcast
    """

    def __init__(self, ip, port, header):
        
        """
        @param [in] ip is IP address of the receiver

        @param [in] port is TCP port

        @param [in] header is boolean for message header 
        
        """
        
        self.header = header
        self.ip = ip
        self.port = port
        try:
            self._connect_socket()
            broadcastLog.debug("Socket connected.")
        except socket.error as e:
            print(e)
            broadcastLog.error("Socket not connected.")
            self.close_and_exit()

    def send(self, message):
        
        """ Tries to send the message via socket 
        
        @param [in] message is an xml VOEvent document

        """
        
        #message = zlib.compress(message, 9)
        #message += "\nEOF\n"
        #print message
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
        """ Connects to a socket """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))
        # print "Connected to %s at port %d" % (self.ip, self.port)
        broadcastLog.info("Connected to %s at port %d" % (self.ip, self.port))

    def _send_and_receive(self, message):
        
        """ Sends a message and receives ack (or some other data) 
        
        @param [in] message is an xml VOEvent document
        
        """
        
        self.sock.send(self._add_voevent_header(message)) if self.header else self.sock.send(message)
        broadcastLog.debug("Message sent")
        data = self.sock.recv(self.BUFFER_SIZE)
        print "received data:", data
        if data == "":
            broadcastLog.warn("Message sent, but echo not received")
        else:
            broadcastLog.debug("Echo received")

class Multicast(Broadcast):

    """
    Class for multicast // to be revised
    """

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

