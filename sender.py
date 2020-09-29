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
seq_num = 0
for server_address in server_addresses:
  received_fin_ack = False
  while(not received_fin_ack):
    data = None
    while data is None:
      try:
        # If already last chunk
        if(len(chunks)-1 == seq_num):
          logging.info(f'Sending packet {seq_num} (FIN) ({len(chunks[seq_num])})')
          # Send file segment
          p = Packet(b'\x02', seq_num, chunks[seq_num])
          sent = s.sendto(p.get_packet_content(), server_address)

          # Wait to receive FIN-ACK Packet
          logging.info(f'Waiting to receive FIN-ACK')
          data, server = s.recvfrom(32774)
          p = Packet(byte_data=data)

          # If received FIN-ACK
          if(p.packet_type == b'\x03'):
            logging.info(f'Received FIN-ACK')
            received_fin_ack = True
        else:
          logging.info(f'Sending packet {seq_num} ({len(chunks[seq_num])})')
          # Send file segment
          p = Packet(b'\x00', seq_num, chunks[seq_num])
          sent = s.sendto(p.get_packet_content(), server_address)
          
          # Wait to receive ACK Packet
          logging.info(f'Waiting to receive ACK')
          data, server = s.recvfrom(32774)
          p = Packet(byte_data=data)

          # If received packet is ACK (\x01)
          if(p.packet_type == b'\x01' and p.get_seq_num() == seq_num):
            logging.info(f'Received ACK')
            seq_num += 1


      except socket.timeout:
        # If ACK not received (packet loss, ack loss)
        logging.info(f'Time out!')
      except:
        logging.info(f'Time out!')


# s.close()