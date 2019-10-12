import struct
import socket


"""
The data is stored as:

dx: 4b float
dy: 4b float
da: 4b float
flags: 1b uint
id: 2b uint
"""
UPDATE_STRUCT_FORMAT = '>fffBH'

class NullSender:
  """
  Doesn't do anything. It's here for duck typing purposes.
  """
  def __init__(self):
    pass

  def send(self, dx, dy, a, kick, dribble):
    pass

class UDPSender:
  """
  Forwards commands from the game to the destination IP
  as a UDP packet.
  """
  def __init__(self, dest_addr):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.dest_addr = dest_addr
    self.next_id = 0

  def send(self, dx, dy, a, kick, dribble):
    flags = (0x02 if kick else 0) | (0x01 if dribble else 0)
    data = struct.pack(UPDATE_STRUCT_FORMAT, dx, dy, a, flags, self.next_id)
    self.next_id = (self.next_id + 1) & 0xffff  # Keep it within 16 bits
    self.socket.sendto(data, self.dest_addr)
