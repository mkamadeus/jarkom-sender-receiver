import socket
from packet import Packet

OUTFILE = "./out/downloaded"

# Input port
# port = int(input())
port = int(input())

# Create UDP based socket (using Datagram Sockets)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(('localhost', port))
print(f'socket binded to {port}')

queue = []
while True:
  data, address = s.recvfrom(32774)
  print(f'Received {len(data)} bytes from {address}')
  
  if(data):
    p = Packet(byte_data=data)

    if (p.generate_checksum() == p.get_checksum()):
      print("Checksum matched. Sending ACK.")
      queue.append((p.seq_num, p.get_message())) 

      # Create ACK packet
      ack = Packet(b'\x01' if p.packet_type != b'\x02' else b'\x03', p.get_seq_num(), b'')

      sent = s.sendto(ack.get_packet_content(), address)
      print(f'Sent {len(data)} back to {address}')

    else:
      print("Checksum unmatched. ACK not sent.")
      
    if(p.packet_type == b'\x02'):
      break

queue.sort()
content = ''
for _,chunk in queue:
  content += chunk

with open(OUTFILE, 'wb') as f:
  f.write(content)

s.close()
