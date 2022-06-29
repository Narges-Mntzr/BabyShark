
from socket import *
from struct import *
import re


def ether(data):
    dest_mac, src_mac, proto = unpack('!6s 6s H', data[:14])
    dest_mac = ':'.join(re.findall('..', dest_mac.encode('hex')))
    src_mac = ':'.join(re.findall('..', src_mac.encode('hex')))

    return [dest_mac, src_mac, hex(proto), data[14:]]


def ip(data):
    maindata = data
    data = unpack('! B s H 2s 2s B B 2s 4s 4s', data[:20])
    return[
        data[0] >> 4,  # version
        "0x" + data[1].encode('hex'),  # header length
        (data[0] & (0x0f)) * 4,  # Diffserv
        data[2],  # total length
        "0x" + data[3].encode('hex'),  # ID
        "0x" + data[4].encode('hex'),  # flags
        data[5],  # ttl
        data[6],  # protocol
        "0x" + data[7].encode('hex'),  # check sum
        inet_ntoa(data[8]),  # source ip
        inet_ntoa(data[9]),  # destination ip
        maindata[(data[0] & (0x0f))*4:],  # ip payload
    ]


def tcp(data):
    TCP_HEADER = unpack("!2H2I4H", data[:20])
    src_port = TCP_HEADER[0]
    dst_port = TCP_HEADER[1]
    seq_num = TCP_HEADER[2]
    ack_num = TCP_HEADER[3]

    data_offset = TCP_HEADER[4] >> 12  # DO

    reserved = (TCP_HEADER[4] >> 6) & 0x03ff  # RSV
    flags = TCP_HEADER[4] & 0x003f
    # 6 bit flags
    urg = (flags & 0x0020)/32
    ack = (flags & 0x0010)/16
    psh = (flags & 0x0008)/8
    rst = (flags & 0x0004)/4
    syn = (flags & 0x0002)/2
    fin = flags & 0x0001

    window = TCP_HEADER[5]
    checksum = TCP_HEADER[6]
    urg_ptr = TCP_HEADER[7]

    return [
        src_port,
        dst_port,
        seq_num,
        ack_num,
        data_offset,
        reserved,
        urg,
        ack,
        psh,
        rst,
        syn,
        fin,
        window,
        checksum,
        urg_ptr
    ]


conn = socket(AF_PACKET, SOCK_RAW, ntohs(0x0003))
while True:
    raw_dat, add = conn.recvfrom(65535)
    ether_shark = ether(raw_dat)
    if(ether_shark[2] == "0x800"):
        ip_shark = ip(ether_shark[3])
        if(ip_shark[7] == 6):
            tcp_shark = tcp(ip_shark[-1])
            if(tcp_shark[7] == 1 and tcp_shark[10] == 1):  # SYN_ACK
                print "port", tcp_shark[0], " is open on", ip_shark[9]
