from packet import Packet
import logging
import socket
import os


logging.basicConfig(format='%(asctime)s %(message)s', datefmt='[%H:%M:%S]', level=logging.INFO)

# Input address receiver
address = input() 

# Input port
port = int(input())

# Input and open file
filename = input()

# Create UDP based socket (using Datagram Sockets)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(5)
server_addresses =[(socket.gethostbyname(add), port) for add in address.split(',')]

filesize = os.stat(filename).st_size

for server_address in server_addresses:
  seq_num = 0
  received_fin_ack = False
  send_fin_count = 0

  with open(filename, 'rb') as f:
    while not received_fin_ack:
      # Read message in chunks
      chunks = f.read(32767)

      # For each chunk...
      data = None
      while data is None:
        try:
          # If already last chunk
          if (filesize <= 32767):
            logging.info(f'Sending packet {seq_num} (FIN) ({len(chunks)})')
            # Send file segment
            p = Packet(b'\x02', seq_num, chunks)
            sent = s.sendto(p.get_packet_content(), server_address)
            send_fin_count += 1

            # Wait to receive FIN-ACK Packet
            logging.info(f'Waiting to receive FIN-ACK')
            data, server = s.recvfrom(32774)
            p = Packet(byte_data=data)

            # If received FIN-ACK
            if(p.packet_type == b'\x03' and p.get_seq_num() == seq_num):
              logging.info(f'Received FIN-ACK')
              received_fin_ack = True
            # or if FIN-ACK can be assumed lost
            else if (send_fin_count > 10):
              logging.info(f'Final timeout: sender will quit')
              logging.info(f'Assuming FIN has been received, FIN-ACK lost')
              received_fin_ack = True

          else:
            logging.info(f'Sending packet {seq_num} ({len(chunks)})')
            # Send file segment
            p = Packet(b'\x00', seq_num, chunks)
            sent = s.sendto(p.get_packet_content(), server_address)
              
            # Wait to receive ACK Packet
            logging.info(f'Waiting to receive ACK')
            data, server = s.recvfrom(32774)
            p = Packet(byte_data=data)

            # If received packet is ACK (\x01)
            if(p.packet_type == b'\x01' and p.get_seq_num() == seq_num):
              logging.info(f'Received ACK')
              seq_num += 1

          # Update how many filesize left to be read
          filesize-= 32767

        except socket.timeout:
          # If ACK not received (packet loss, ack loss)
          logging.info(f'Time out!')
        except:
          logging.info(f'Time out!')

    # s.close()