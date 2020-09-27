import socket

# Input address receiver
# pls

# Input port
port = int(input())

# Input file name
filename = input()

with open(filename, 'rb') as f:
  message = f.read()
  # message = b'lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet'

# Create UDP based socket (using Datagram Sockets)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(3)
server_address =('localhost', 3000)

data = ''
while not data:
  try:
    print(f'sending')
    sent = s.sendto(message, server_address)

    print(f'waiting to receive')
    data, server = s.recvfrom(4096)

    print(f'received {data}')

  except socket.timeout:
    print(f'time out!')

s.close()