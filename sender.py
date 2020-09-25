import socket

# Input port
port = int(input())

# Create UDP based socket (using Datagram Sockets)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address =('localhost', 3000)
message = b'lorem ipsum dolor sit amet'


try:
  print(f'sending')
  sent = s.sendto(message, server_address)

  print(f'waiting to receive')
  data, server = s.recvfrom(4096)

  print(f'received {data}')

finally:
  s.close()