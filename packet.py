import math
import struct
from utility import bytearray_to_binary, bytearray_to_int, int_to_bytes, bytes_to_binary, bytes_to_int

class Packet:

  # Type = 8 bit = 1 bytes
  # Length = 16 bit = 2 bytes (unsigned integer)
  # Sequence Number = 16 bit = 2 bytes
  # Checksum = 16 bit = 2 bytes
  # Data = 32767 bytes (2^15-1)

  # packet_type : \x00 (DATA) \x01 (ACK) \x02 (FIN) \x03 (FIN_ACK)
  # seq_num : integer
  # data : in bytes with limit of 32767 bytes
  def __init__(self, packet_type=None, seq_num=None, data=None, byte_data=None):

    # Check if packet exceeded limit

    if(byte_data is not None):
      self.packet_type = struct.pack('s', byte_data[:1])
      self.data_length = struct.pack('2s', byte_data[1:3])
      self.seq_num = struct.pack('2s', byte_data[3:5])
      self.checksum = struct.pack('2s', byte_data[5:7])
      self.data = struct.pack(f'{len(byte_data[7:])}s', byte_data[7:])
      return

    if(len(data) > 32767):
      raise Exception('Packet contents too long')

    self.packet_type = struct.pack('s', packet_type)
    self.data_length = struct.pack('2s', len(data).to_bytes(2, 'little'))
    self.seq_num = struct.pack('2s', seq_num.to_bytes(2, 'little'))
    self.data = struct.pack(f'{len(data)}s', data)
    self.checksum = struct.pack('2s', self.generate_checksum())

    self.packet_content = self.packet_type + self.data_length + self.seq_num + self.checksum + self.data

  def generate_checksum(self):
    content = bytearray(self.packet_type + self.data_length + self.seq_num + self.data)
    if(len(content) % 2 != 0):
      content += b'\x00'
    checksum = bytearray(b'\0\0')
    for i in range(0, math.ceil((len(content))/2)):
      checksum[0] ^= content[2*i]
      checksum[1] ^= content[2*i+1]

    return bytes(checksum)

  # GETTERS
  def get_data_length(self):
    return struct.unpack('h', self.data_length)[0]

  def get_packet_type(self):
    return struct.unpack('b', self.packet_type)[0]
  
  def get_seq_num(self):
    return struct.unpack('h', self.seq_num)[0]

  def get_message(self):
    return struct.unpack(f'{self.get_data_length()}s' ,self.data)[0]

  def get_checksum(self):
    return self.checksum
  
  def get_packet_content(self):
    return self.packet_content

  # OUTPUT  
  def print_packet_info(self):
    print(f'type = {self.packet_type} ({self.get_packet_type()})')
    print(f'length = {self.data_length} ({self.get_data_length()})')
    print(f'seq_num = {self.seq_num} ({self.get_seq_num()})')
    print(f'checksum = {self.checksum}')
    print(f'data = {self.data[0:self.get_data_length()]}')
