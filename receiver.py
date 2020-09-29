import socket
from packet import Packet
import logging
# import time
# import random

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
while True:
  data, address = s.recvfrom(32774)
  logging.info(f'Received {len(data)} bytes from {address}')
  
  if(data):
    p = Packet(byte_data=data)

    if (p.generate_checksum() == p.get_checksum()):
      logging.info("Checksum matched")
      queue.append((p.seq_num, p.get_message())) 

      # Create ACK packet
      ack = Packet(b'\x01' if p.packet_type != b'\x02' else b'\x03', p.get_seq_num(), b'')
      # time.sleep(random.random()*6)
      sent = s.sendto(ack.get_packet_content(), address)
      logging.info(f'Sent ACK to {address}')

    else:
      logging.info("Checksum mismatch, ACK not sent")
      
    if(p.packet_type == b'\x02'):
      logging.info("FIN packet found, stopping")
      break

queue.sort()
content = b''
for _,chunk in queue:
  content += chunk

with open(outfile, 'wb') as f:
  f.write(content)

s.close()
