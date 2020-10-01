import socket
from packet import Packet
import logging
import time
import random

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='[%H:%M:%S]', level=logging.INFO)

outfile = "./out/downloaded"

# Input port
port = int(input())

# Create UDP based socket (using Datagram Sockets)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address =(socket.gethostbyname(socket.gethostname()), port)

s.bind(server_address)
logging.info(f'Socket binded to {server_address}')

queue = []
received = []
while True:
  data, address = s.recvfrom(32774)
  if(data):
    p = Packet(byte_data=data)
    if(p.get_seq_num() in received):
      if(p.packet_type == b'\x02'):
        ack = Packet(b'\x03', p.get_seq_num(), b'')
        sent = s.sendto(ack.get_packet_content(), address)
        break
      else:
        ack = Packet(b'\x01', p.get_seq_num(), b'')
        sent = s.sendto(ack.get_packet_content(), address)

    elif(p.get_seq_num() not in received and p.get_checksum() == p.generate_checksum()):
      if(p.packet_type == b'\x02'):
        logging.info(f'Checksum matched for packet {p.get_seq_num()}')
        queue.append((p.get_seq_num(), p.get_message()))
        received.append(p.get_seq_num())

        ack = Packet(b'\x03', p.get_seq_num(), b'')
        sent = s.sendto(ack.get_packet_content(), address)
        break
      else:
        logging.info(f'Checksum matched for packet {p.get_seq_num()}')
        queue.append((p.get_seq_num(), p.get_message()))
        received.append(p.get_seq_num())

        ack = Packet(b'\x01', p.get_seq_num(), b'')
        sent = s.sendto(ack.get_packet_content(), address)
# Reset file
open(outfile, 'w').close()

with open(outfile, 'ab') as f:
  queue.sort()
  for _, msg in queue:
    f.write(msg)

    

    



s.close()

