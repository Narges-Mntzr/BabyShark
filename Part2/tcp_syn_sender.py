
from socket import inet_aton

fd = open('info.txt', 'r')
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
src_ip = inet_aton(Lines[2]).encode("hex")  # source ip
dest_ip = inet_aton(Lines[0]).encode("hex")  # dest ip
src_port = "%04x" % int(Lines[3])  # src port
dest_port = "%04x" % int(Lines[1])  # dest port
seq_num = "17 49 30 d1"  # seq number
ack = "00 00 00 00"  # ack number
h_len = "50 02" # tcp header length and flags ("a0 02" for 40 bytes, "50 02" for 20 bytes)
w_size = "72 10"  # window size
cs4 = "00 00"  # tcp check sum
up = "00 00"  # urgent pointer

interface0 = Lines[4].strip()
