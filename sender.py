import socket
from packet import Packet
from utility import bytearray_to_binary, bytearray_to_int, int_to_bytes, bytes_to_binary, bytes_to_int

# Input address receiver
address = input() 

# Input port
port = int(input())

# Input file name
filename = input()

with open(filename, 'rb') as f:
  message = f.read()
  # message = b'lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet'

# Create UDP based socket (using Datagram Sockets)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(3)
server_address =('localhost', 3000)

data = ''
while not data:
  try:
    print(f'sending')
    p = Packet(b'\x00', 1, message)
    p.print_packet_info()

    sent = s.sendto(p.get_packet_content(), server_address)

    print(f'waiting to receive')
    data, server = s.recvfrom(32774)

    p = Packet(byte_data=data)
    if(p.packet_type == b'\x01'):
      print(f'received ACK')

  except socket.timeout:
    print(f'time out!')

s.close()