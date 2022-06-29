from socket import *
from binascii import unhexlify, hexlify
from checksum3 import cs

fd = open('./info.txt', 'r')
Lines = fd.readlines()

dest_mac = Lines[6][:17]  # destination mac
src_mac = Lines[5][:17]  # source mac
proto3 = "08 00"  # layer 3 protocol number
ver = "45"  # version, header lengh
diff = "00"  # diffserv
t_len = "00 28"  # total length ("00 28" for 40bytes, "00 3c" for 60 bytes)
id = "07 c3"  # id
flags = "40 00"  # flags
ttl = "40"  # ttl
proto4 = "06"  # layer 4 protocol number
cs3 = "00 00"  # ip check sum

src_ip = hexlify(inet_aton(Lines[2])).decode()  # source ip
src_ip = src_ip[:2] + " " + src_ip[2:4] + " " + src_ip[4:6] + " " + src_ip[6:]

dest_ip = hexlify(inet_aton(Lines[0])).decode()  # dest ip
dest_ip = dest_ip[:2] + " " + dest_ip[2:4] + \
    " " + dest_ip[4:6] + " " + dest_ip[6:]

src_port = "%04x" % int(Lines[3])  # src port
src_port = src_port[:2] + " " + src_port[2:]

dest_port = "%04x" % int(Lines[1])  # dest port
dest_port = dest_port[:2] + " " + dest_port[2:]

seq_num = "17 49 30 d1"  # seq number
ack = "00 00 00 00"  # ack number
# tcp header length and flags ("a0 02" for 40 bytes, "50 02" for 20 bytes)
h_len = "50 02"
w_size = "72 10"  # window size
cs4 = "00 00"  # tcp check sum
up = "00 00"  # urgent pointer

interface0 = Lines[4].strip()

# ethernet
ethernet_header = f'{dest_mac} {src_mac} {proto3}'

# ip_header
ip_header = f'{ver} {diff} {t_len} '
ip_header += f'{id} {flags} '
ip_header += f'{ttl} {proto4} {cs3} '
ip_header += f'{src_ip} '
ip_header += f'{dest_ip}'

checksum = cs(ip_header)
ip_header = ip_header[:30] + checksum[:2] + \
    " " + checksum[2:]+" " + ip_header[36:]

# tcp_header
tcp_header = f'{src_port} {dest_port} '
tcp_header += f'{seq_num} '
tcp_header += f'{ack} '
tcp_header += f'{h_len} {w_size} '
tcp_header += f'{cs4} {up} '

# pseudo header
pseudo_header = f'{src_ip} '
pseudo_header += f'{dest_ip} '
pseudo_header += f'00 {proto4} 00 14 '

pseudo_header = pseudo_header + tcp_header
checksum = cs(pseudo_header)
print(checksum)

tcp_header = tcp_header[:47] + " " + checksum[:2] + \
    " " + checksum[2:4]+" " + tcp_header[54:]


packet = ethernet_header+" " + ip_header + " " + tcp_header
packet = "".join(packet.split())

# send pkt
pkt_byte = unhexlify((packet))
# try:
#     s = socket(AF_PACKET, SOCK_RAW)
#     s.bind((interface0, 0))
#     s.send(pkt_byte)
#     print(f'Sent {len(pkt_byte)}-byte packet on {interface0}')
# except:
#     print(f'Something went wrong!!!')
