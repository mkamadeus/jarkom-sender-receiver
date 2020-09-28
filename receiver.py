import socket
from packet import Packet

OUTFILE = "./out/downloaded"

# Input port
# port = int(input())
port = 3000

# Create UDP based socket (using Datagram Sockets)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(('localhost', port))
print(f'socket binded to {port}')

while True:
  data, address = s.recvfrom(32774)
  print(f'Received {len(data)} bytes from {address}')
  
  if(data):
    p = Packet(byte_data=data)
    p.print_packet_info()

    # Create ACK packet
    ack = Packet(b'\x01', p.get_seq_num(), b'')

    sent = s.sendto(ack.get_packet_content(), address)
    print(f'sent {len(data)} back to {address}')

    with open(OUTFILE, 'wb') as f:
      f.write(p.get_message())
  # client, address = s.accept()
  # print(f'Got connection from {address}')
s.close()
  # client.send('yey')
  # client.close()
