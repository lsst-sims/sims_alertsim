from __future__ import with_statement
import sys
import socket
import subprocess
import argparse

__all__ = ["TCPReceiver"]

class TCPReceiver(object):
    """
    A simple tcp receiver which accepts messages (VOEvents) 
    and returns acknowledgement

    @param [in] port is a TCP port
    
    """

    def __init__(self, port):
        self._output_to_file = False
        self._file_name = None
        self._connection = None
        # more effective than // TCP_IP = os.popen("hostname -i").read()
        #TCP_IP = subprocess.check_output("hostname -i", shell=True)

        #default ip address
        TCP_IP = '127.0.0.1'

        #determine local ip address

        #works on mac
        if sys.platform == 'darwin':
            TCP_IP = socket.gethostbyname(socket.gethostname())
        else:
        #works on linux, at least OpenSuSE
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
            TCP_IP = s.getsockname()[0]

        TCP_PORT = port
        self.BUFFER_SIZE = 10000  # Normally 1024, but we want fast response

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)

        print 'My address:', TCP_IP

        self._connection, addr = s.accept()
        print 'Connection address:', addr

    def output_to_file(self, file_name):
        self._output_to_file = True
        self._file_name = file_name

    def close_connection(self):
        if self._connection is not None:
            self._connection.close()
        self._connection = None

    def _listen(self, file_handle=None):
        while 1:
            data = self._connection.recv(self.BUFFER_SIZE)
            if not data: break
            header = data[0:4]
            if file_handle is not None:
                file_handle.write(data)
            print "header:", header
            print "received data:", data[4:]
            self._connection.send(header)  # echo


    def listen(self):
        if self._connection is None:
            raise RuntimeError("There is no connection to listen to")

        if self._output_to_file:
            with open(self._file_name, "w") as file_handle:
               self._listen(file_handle=file_handle)
        else:
            self._listen()

        self.close_connection()

#command line parser for tcp port
PARSER = argparse.ArgumentParser(description = "")
PARSER.add_argument("-p", "--port", type=int, default='8098',
        help="tcp port")
ARGS = PARSER.parse_args()

if __name__ == "__main__":
    receiver = TCPReceiver(ARGS.port)
    receiver.output_to_file("VOEvents.txt")
    receiver.listen()
    receiver.close_connection()
