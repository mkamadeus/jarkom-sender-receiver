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

# content = b''
last_seq_num = -1
last_data = b''
# Reset file
open(outfile, 'w').close()

fin = False
received = []
while not fin:
  logging.info(f'Waiting to receive data')
  try:
    data, address = s.recvfrom(32774)
  except:
    # # Sender closed
    # logging.info(f'Writing data from packet {last_seq_num}')
    # with open(outfile, 'ab') as f:
    #   f.write(last_data)
    break

  logging.info(f'Received {len(data)} bytes from {address}')
  
  if(data):
    p = Packet(byte_data=data)

    if (p.get_seq_num() in received):
      # Resend ACK if seq_num have been received before
      # Means the ACK for that seq_num is lost
      ack = Packet(b'\x01', p.get_seq_num(), b'')
      sent = s.sendto(ack.get_packet_content(), address)
      logging.info(f'Packet received before. Resent ACK to {address}')

    else:
      # Ok, a new packet
      if (p.generate_checksum() == p.get_checksum()):
        logging.info(f'Checksum matched for packet {p.get_seq_num()}')

        if(p.get_seq_num() == last_seq_num + 1):
          logging.info(f'Writing data from packet {last_seq_num} ({len(last_data)})')
          with open(outfile, 'ab') as f:
            f.write(last_data)

          last_seq_num = p.get_seq_num()
          last_data = p.get_message()
          received.append(p.get_seq_num())

        # Delay for testing
        # time.sleep(random.random()*10)

        if(p.packet_type == b'\x02'):
          # Create FIN-ACK packet
          ack = Packet(b'\x03', p.get_seq_num(), b'')
          sent = s.sendto(ack.get_packet_content(), address)
          logging.info(f'Sent FIN-ACK to {address}')
          if(not fin):
            logging.info(f'Writing data from packet {last_seq_num} ({len(last_data)})')
            with open(outfile, 'ab') as f:
              f.write(last_data)
            fin=True

        else:
          # Create ACK packet
          ack = Packet(b'\x01', p.get_seq_num(), b'')
          sent = s.sendto(ack.get_packet_content(), address)
          logging.info(f'Sent ACK to {address}')
        # ack = Packet(b'\x01' if p.packet_type != b'\x02' else b'\x03', p.get_seq_num(), b'')
        # sent = s.sendto(ack.get_packet_content(), address)
        # logging.info(f'Sent ACK to {address}')

      else:
        logging.info("Checksum mismatch, ACK not sent")
      
    # if(p.packet_type == b'\x02'):
    #   logging.info("FIN packet found")
      # break

# with open(outfile, 'wb') as f:
#   f.write(content)

s.close()
