import sys
import socket
import subprocess
import argparse

def main(port):

    # more effective than // TCP_IP = os.popen("hostname -i").read()
    TCP_IP = subprocess.check_output("hostname -i", shell=True)
    TCP_PORT = port
    BUFFER_SIZE = 10000  # Normally 1024, but we want fast response

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    print 'My address:', TCP_IP

    conn, addr = s.accept()
    print 'Connection address:', addr
    f = open("VOEvents.txt", 'w')
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        header = data[0:4]
        f.write("data")
        print "header:", header
        print "received data:", data[4:]
        conn.send(header)  # echo
    f.close()
    conn.close()

PARSER = argparse.ArgumentParser(description = "")
PARSER.add_argument("-p", "--port", type=int, default='8098',
        help="tcp port")
ARGS = PARSER.parse_args()

if __name__ == "__main__":
    sys.exit(main(ARGS.port))
