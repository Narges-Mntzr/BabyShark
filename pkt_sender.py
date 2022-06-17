from socket import *

# Receive the message and convert it to binary
message = input("What is your packet content? ")
pkt_bin = bin(int(message, 16))[2:]
pkt_byte = bytes([int(i) for i in pkt_bin])
# pkt_byte = unhexlify((pkt_bin))

# Send packet
interfaceName = input("Which interface do you want to use?")
try:
    s = socket(AF_PACKET, SOCK_RAW)
    s.bind((interfaceName, 0))
    s.send(pkt_byte)
    print(pkt_byte)
    print(f'Sent {len(pkt_byte)}-byte packet on {interfaceName}')
except:
    print(f'Something went wrong!!!')
