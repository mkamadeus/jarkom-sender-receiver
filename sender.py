from packet import Packet
import socket

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
s.settimeout(3)
server_address =('localhost', 3000)

# For each chunk...
for seq_num, chunk in enumerate(chunks):
  data = None
  while data is None:
    try:
      # Send file segment
      print(f'Sending packet {seq_num}')
      p = Packet(b'\x00' if len(chunks)-1 != seq_num else b'\x02', seq_num, chunk)
      sent = s.sendto(p.get_packet_content(), server_address)

      # Wait to receive ACK Packet
      print(f'Waiting to receive')
      data, server = s.recvfrom(32774)
      p = Packet(byte_data=data)

      # If received packet is ACK (\x01)
      if(p.packet_type == b'\x01'):
        print(f'Received ACK')

    except socket.timeout:
      # If ACK not received (packet loss, ack loss)
      print(f'Time out!')

s.close()