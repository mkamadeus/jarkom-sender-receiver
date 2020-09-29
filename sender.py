from packet import Packet
import logging
import socket


logging.basicConfig(format='%(asctime)s %(message)s', datefmt='[%H:%M:%S]', level=logging.INFO)

# Input address receiver
address = input() 

# Input port
port = int(input())

# Input and open file
filename = input()
with open(filename, 'rb') as f:
  message = f.read()

# Split message into smaller chunks
chunks = [message[i:i+32767] for i in range(0, len(message), 32767)]

# Create UDP based socket (using Datagram Sockets)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(5)
server_addresses =[(socket.gethostbyname(add), port) for add in address.split(',')]

# For each chunk...
for server_address in server_addresses:
  for seq_num, chunk in enumerate(chunks):
    data = None
    while data is None:
      try:
        # Send file segment
        logging.info(f'Sending packet {seq_num}')
        p = Packet(b'\x00' if len(chunks)-1 != seq_num else b'\x02', seq_num, chunk)
        sent = s.sendto(p.get_packet_content(), server_address)

        # Wait to receive ACK Packet
        logging.info(f'Waiting to receive ACK')
        data, server = s.recvfrom(32774)
        p = Packet(byte_data=data)

        # If received packet is ACK (\x01)
        if(p.packet_type == b'\x01'):
          logging.info(f'Received ACK')
        
        if(p.packet_type == b'\x03'):
          logging.info(f'Received FIN-ACK')

      except socket.timeout:
        # If ACK not received (packet loss, ack loss)
        logging.info(f'Time out!')

s.close()