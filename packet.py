import math
import struct
from utility import bytearray_to_binary, bytearray_to_int, int_to_bytes, bytes_to_binary, bytes_to_int

class Packet:

  # Type = 8 bit = 1 bytes
  # Length = 16 bit = 2 bytes (unsigned integer)
  # Sequence Number = 16 bit = 2 bytes
  # Checksum = 16 bit = 2 bytes
  # Data = 32767 bytes (2^15-1)
  def __init__(self, data_type, data_length, seq_num, data):
    self.data_type = struct.pack('s', data_type)
    self.data_length = struct.pack('2s', data_length)
    self.seq_num = struct.pack('2s', seq_num)
    self.data = struct.pack('32767s', data)
    self.checksum = struct.pack('2s', self.generate_checksum())

  def generate_checksum(self):
    content = bytearray(self.data_type + self.data_length + self.seq_num + self.data)
    checksum = bytearray(b'\0\0')
    for i in range(0, math.ceil((5 + self.get_data_length())/2)):
      checksum[0] ^= content[2*i]
      checksum[1] ^= content[2*i+1]

    return bytes(checksum)

  # GETTERS
  def get_data_length(self):
    return struct.unpack('h', self.data_length)[0]

  def get_data_type(self):
    return struct.unpack('b', self.data_type)[0]
  
  def get_seq_num(self):
    return struct.unpack('h', self.seq_num)[0]
  
  def get_packet_content(self):
    return self.data_type + self.data_length + self.seq_num + self.data

  # OUTPUT  
  def print_packet_info(self):
    print(f'type = {self.data_type} ({self.get_data_type()})')
    print(f'length = {self.data_length} ({self.get_data_length()})')
    print(f'seq_num = {self.seq_num} ({self.get_seq_num()})')
    print(f'checksum = {self.checksum}')
    print(f'data = {self.data[0:self.get_data_length()]}')
