import struct
import socket


"""
The data is stored as:
Big Endian
dx: 4b float, pos error
dy: 4b float, pos error
vx: 4b float, velocity
vy: 4b float, velocity
da: 4b float, angular error
w: 4b float, (it's an omega) angular velocity
flags: 1b uint, see below
id: 2b uint, a "unique" packet identifier for preventing out-of-order packets

The bits inside flags represent, from LSB to MSB:
- Should dribble
- Should kick
"""
UPDATE_STRUCT_FORMAT = '>ffffffBH'

class NullSender:
  """
  Doesn't do anything. It's here for duck typing purposes.
  """
  def __init__(self):
    pass

  def send(self, dx, dy, vx, vy, a, w, kick, dribble):
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

  def send(self, dx, dy, vx, vy, a, w, kick, dribble):
    flags = (0x02 if kick else 0) | (0x01 if dribble else 0)
    data = struct.pack(UPDATE_STRUCT_FORMAT, dx, dy, vx, vy, a, w, flags, self.next_id)
    self.next_id = (self.next_id + 1) & 0xffff  # Keep it within 16 bits
    self.socket.sendto(data, self.dest_addr)
