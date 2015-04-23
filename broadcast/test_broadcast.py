import socket


TCP_IP = '147.91.240.26'
TCP_PORT = 8099
BUFFER_SIZE = 10000
MESSAGE = "x" * 3000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while 1:
    s.send(MESSAGE)
    data = s.recv(BUFFER_SIZE)
s.close()

print "received data:", data
