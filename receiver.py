import socket

# Input port
# port = int(input())
port = 3000

# Create UDP based socket (using Datagram Sockets)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(('localhost', port))
print(f'socket binded to {port}')

# s.listen(5)
# print('socket listening')


while True:
  data, address = s.recvfrom(4096)
  print(f'Received {len(data)} bytes from {address}')
  print(data)

  if(data):
    sent = s.sendto(data, address)
    print(f'sent {len(data)} back to {address}')
    s.close()
    break
  # client, address = s.accept()
  # print(f'Got connection from {address}')
  # client.send('yey')
  # client.close()

