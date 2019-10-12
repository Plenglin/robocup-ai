import struct
import socket

UPDATE_STRUCT_FORMAT = '>fffBH'
PORT = 52343

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.bind(('127.0.0.1', PORT))

while True:
  data, _ = sock.recvfrom(1024)
  print(struct.unpack(UPDATE_STRUCT_FORMAT, data))
