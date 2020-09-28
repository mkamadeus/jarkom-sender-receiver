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

print(len(message))

splitted = [message[i:i+32767] for i in range(0, len(message), 32767)]

# Create UDP based socket (using Datagram Sockets)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(3)
server_address =('localhost', 3000)

for seqnum, split in enumerate(splitted):
  data = ''
  while not data:
    try:
      print(f'Sending packet {seqnum}')
      p = Packet(b'\x00' if len(splitted)-1 != seqnum else b'\x02', seqnum, split)

      sent = s.sendto(p.get_packet_content(), server_address)

      print(f'Waiting to receive')
      data, server = s.recvfrom(32774)

      p = Packet(byte_data=data)
      if(p.packet_type == b'\x01'):
        print(f'Received ACK')

    except socket.timeout:
      print(f'Time out!')

s.close()