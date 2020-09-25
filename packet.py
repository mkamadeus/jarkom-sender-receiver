import math
from utility import bytearray_to_binary, bytearray_to_int, int_to_bytes

class Packet:

  # Type = 8 bit = 1 bytes
  # Length = 16 bit = 2 bytes (unsigned integer)
  # Seqnum = 16 bit = 2 bytes
  # Checksum = 16 bit = 2 bytes
  # Data = 32767 bytes (2^15-1)
  def __init__(self, data_type, data_length, seqnum, data):
    self.data_type = bytearray(data_type, 'utf-8')
    self.data_length = bytearray(data_length)
    self.seqnum = bytearray(seqnum)
    self.data = bytearray(data, 'utf-8') + (b'\0'*(32767 - len(data)))
    self.checksum = self.generate_checksum()

  def generate_checksum(self):
    content = self.data_type + self.data_length + self.seqnum + self.data
    checksum = bytearray('\0\0', 'utf-8')
    for i in range(0, math.ceil((5 + self.get_data_length())/2)):
      # print(bytearray_to_binary(checksum))
      # print(bytearray_to_binary(content[2*i:2*i+2]))
      # print('----------')
      checksum[0] ^= content[2*i]
      checksum[1] ^= content[2*i+1]
      # print(bytearray_to_binary(checksum))
      # print()

    return checksum

  def get_data_length(self):
    return bytearray_to_int(self.data_length)

  def print_packet_info(self):
    print(f'type = {bytearray_to_binary(self.data_type)} ({self.data_type.decode()})')
    print(f'length = {bytearray_to_binary(self.data_length)} ({self.data_length.decode()})')
    print(f'seqnum = {bytearray_to_binary(self.seqnum)} ({self.seqnum.decode()})')
    print(f'checksum = {bytearray_to_binary(self.checksum)}')
    print(f'data = {bytearray_to_binary(self.data[0:self.get_data_length()])} ({self.data[0:self.get_data_length()].decode()})')

  def print_packet_data(self):  
    print(f'{bytearray_to_binary(self.data_type)} {bytearray_to_binary(self.data_length)} {bytearray_to_binary(self.seqnum)} {bytearray_to_binary(self.checksum)} {bytearray_to_binary(self.data[0:self.get_data_length()])}')



message = 'Lorem ipsum dolor sit amet'
print(int_to_bytes(3))
p = Packet('i',int_to_bytes(len(message)),int_to_bytes(1), message)
p.print_packet_info()
p.print_packet_data()
