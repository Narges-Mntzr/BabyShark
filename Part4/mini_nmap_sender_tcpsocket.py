from threading import Thread
from make_pkt import make_pkt
from socket import *
import argparse
from binascii import unhexlify, hexlify

signal = 0

# setup
fd = open('./info.txt', 'r')
Lines = fd.readlines()
interface0 = Lines[4].strip()

class mySocket(Thread):
    def __init__(self, port):
        Thread.__init__(self)
        self.port = port
        self.sock = socket(AF_PACKET, SOCK_RAW)

    def run(self):
        global signal    #made global here
        while True:
            if signal == 1:
                pkt_byte = unhexlify((make_pkt(self.port)))
                try:

                    self.sock.bind((interface0, 0))
                    self.sock.send(pkt_byte)
                    print(f'Sent TCP SYN packet to port {self.port}')
                except:
                    print(f'Something went wrong!!!')
                finally:
                    break



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='args')

    parser.add_argument('-min', default=0, type=int,
                        help='minimum target port')
    parser.add_argument('-max', default=65535, type=int,
                        help='maximum target port')
    args = parser.parse_args()
    a = args.min
    b = args.max

    for i in range(a,b):
        x = mySocket(i)
        x.start()
  
    signal = 1

