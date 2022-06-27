
from socket import *
import string
from checksum3 import header_checksum
import argparse

#setup
fd = open('./info.txt', 'r')
Lines = fd.readlines()
interface0 = Lines[4].strip()

def make_pkt(destination_port):
    dest_mac = Lines[6][:17]  # destination mac
    src_mac = Lines[5][:17]  # source mac
    proto3 = "08 00"  # layer 3 protocol number
    ver = "45"  # version, header lengh
    diff = "00"  # diffserv
    t_len = "00 3c"  # total length ("00 28" for 40bytes, "00 3c" for 60 bytes)
    id = "07 c3"  # id
    flags = "40 00"  # flags
    ttl = "40"  # ttl
    proto4 = "06"  # layer 4 protocol number
    cs3 = "00 00"  # ip check sum

    src_ip = Lines[2].split('.')
    src_ip = ''.join((hex(int(i))[2:] for i in src_ip))  # source ip

    dest_ip = Lines[0].split('.')
    dest_ip = ''.join((hex(int(i))[2:] for i in dest_ip))  # dest ips

    src_port = "%04x" % int(Lines[3])  # src port
    dest_port = "%04x" % int(destination_port)  # dest port
    seq_num = "17 49 30 d1"  # seq number
    ack = "00 00 00 00"  # ack number
    # tcp header length and flags ("a0 02" for 40 bytes, "50 02" for 20 bytes)
    h_len = "a0 02"
    w_size = "72 10"  # window size
    cs4 = "00 00"  # tcp check sum
    up = "00 00"  # urgent pointer


    # ip_header
    ip_header = f'{ver}{diff}{t_len}'
    ip_header += f'{id}{flags}'
    ip_header += f'{ttl}{proto4}{cs3}'
    ip_header += f'{src_ip}'
    ip_header += f'{dest_ip}'
    ip_header += f'{src_port}{dest_port}'
    ip_header += f'{seq_num}'
    ip_header += f'{ack}'
    ip_header.translate({ord(c): None for c in string.whitespace})

    ip_header = bytes.fromhex(ip_header)

    checksum = hex(header_checksum(ip_header, len(ip_header)))

    ip_header = ip_header.hex()
    ip_header = ip_header[:20] + checksum[2:] + ip_header[24:]


    # tcp_header
    tcp_header = f'{src_port} {dest_port}'
    tcp_header += f'{seq_num}'
    tcp_header += f'{ack}'
    tcp_header += f'{h_len} {w_size}'
    tcp_header += f'{cs4} {up}'
    tcp_header.replace(" ", "")
    tcp_header = bytes.fromhex(tcp_header)

    # pseudo header
    pseudo_header = f'{src_mac}'
    pseudo_header += f'{dest_mac}'
    pseudo_header += f'{proto3} {hex(len(tcp_header))[2:]}'
    pseudo_header.replace(" ", "")
    pseudo_header = bytes.fromhex(pseudo_header)

    pseudo_header = pseudo_header + tcp_header
    checksum = hex(header_checksum(pseudo_header, len(pseudo_header)))

    tcp_header = tcp_header.hex()
    tcp_header = tcp_header[:32] + checksum[2:] + tcp_header[36:]

    packet = ip_header + tcp_header
    print(packet)
    return packet


# send pkt
def main(a,b):
    for i in range(a,b):
        pkt_bin = bin(int(make_pkt(i), 16))[2:]
        pkt_byte = bytes([int(i) for i in pkt_bin])


        try:
            s = socket(AF_PACKET, SOCK_RAW)
            s.bind((interface0, 0))
            # print(pkt_byte)
            print(f'Sent {len(pkt_byte)}-byte packet on {interface0}')
        except:
            print(f'Something went wrong!!!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='args')

    parser.add_argument('-min', default=0, type=int,
                        help='first player path')
    parser.add_argument('-max', default=65535, type=int,
                        help='second player path')
    args = parser.parse_args()
    a = args.min
    b = args.max

    main(a,b)

