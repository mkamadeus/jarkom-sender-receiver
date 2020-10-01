from packet import Packet
import logging
import socket
import os
import threading

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

def sender_function(server_address, seq_num, message):
    try:
        logging.info(f'Sending {seq_num}')
        p = Packet(b'\x00', seq_num, message)
        s.sendto(p.get_packet_content(), server_address)

        # logging.info(f'Waiting')
        # data, server = s.recvfrom(32744)
        # p = Packet(byte_data=data)
        # if(p.packet_type == b'\x01' and p.get_seq_num() == seq_num):
        #     logging.info(f'Received ACK')
        #     break
    except:
        logging.info('Timeout')


with open(filename, 'rb') as f:
    message = f.read()
    chunks = [message[i:i+32767] for i in range(0, len(message), 32767)]

for server_address in server_addresses:
    received  = [False for i in range(len(chunks))]
    while True:
        threads = []
        for i, chunk in enumerate(chunks):
            if(i == len(chunks)-1):
                break        
            
            if(not received[i]):
                t = threading.Thread(target=sender_function, args=(server_address, i, chunk))
                threads.append(t)
                t.start()
        
        if(len(threads) == 0):
            break

        for thread in threads:
            thread.join()

        while True:
            try:
                logging.info(f'Waiting to receive ACK')
                data, server = s.recvfrom(32744)
                p = Packet(byte_data=data)
                if(p.packet_type == b'\x01'):
                    received[p.get_seq_num()] = True
                    logging.info(f'Received ACK for {p.get_seq_num()}')
            except:
                logging.info('Timeout')
                break
    
    while True:
        try:
            logging.info(f'Sending {len(chunks)-1}')
            p = Packet(b'\x02', len(chunks)-1, chunks[len(chunks)-1])
            s.sendto(p.get_packet_content(), server_address)

            logging.info(f'Waiting')
            data, server = s.recvfrom(32744)
            p = Packet(byte_data=data)
            if(p.packet_type == b'\x03' and p.get_seq_num() == len(chunks)-1):
                logging.info(f'Received ACK')
                break
        except:
            pass
    # logging.info(f'Sending {len(chunks)-1}')
    # p = Packet(b'\x02', len(chunks)-1, chunks[len(chunks)-1])
    # s.sendto(p.get_packet_content(), server_address)

    # logging.info(f'Waiting')
    # data, server = s.recvfrom(32744)
    # p = Packet(byte_data=data)
    # if(p.packet_type == b'\x03' and p.get_seq_num() == len(chunks)-1):
    #     logging.info(f'Received FIN-ACK')


    
# for server_address in server_addresses:
#   filesize = os.stat(filename).st_size
#   seq_num = 0
#   received_fin_ack = False
#   send_fin_count = 0

#   with open(filename, 'rb') as f:
#     while not received_fin_ack:
#       # Read message in chunks
#       chunks = f.read(32767)

#       # For each chunk...
#       data = None
#       while data is None:
#         try:
#           # If already last chunk
#           if (filesize <= 32767):
#             logging.info(f'Sending packet {seq_num} (FIN) ({len(chunks)})')
#             # Send file segment
#             p = Packet(b'\x02', seq_num, chunks)
#             sent = s.sendto(p.get_packet_content(), server_address)
#             send_fin_count += 1

#             # FIN-ACK can be assumed lost
#             if (send_fin_count > 12):
#               logging.info(f'Final timeout: sender will quit')
#               logging.info(f'Assuming FIN has been received & FIN-ACK is lost')
#               received_fin_ack = True
#               break

#             # Wait to receive FIN-ACK Packet
#             logging.info(f'Waiting to receive FIN-ACK')
#             data, server = s.recvfrom(32774)
#             p = Packet(byte_data=data)

#             # If received FIN-ACK
#             if(p.packet_type == b'\x03' and p.get_seq_num() == seq_num):
#               logging.info(f'Received FIN-ACK')
#               received_fin_ack = True

#           else:
#             logging.info(f'Sending packet {seq_num} ({len(chunks)})')
#             # Send file segment
#             p = Packet(b'\x00', seq_num, chunks)
#             sent = s.sendto(p.get_packet_content(), server_address)
              
#             # Wait to receive ACK Packet
#             logging.info(f'Waiting to receive ACK')
#             data, server = s.recvfrom(32774)
#             p = Packet(byte_data=data)

#             # If received packet is ACK (\x01)
#             if(p.packet_type == b'\x01' and p.get_seq_num() == seq_num):
#               logging.info(f'Received ACK')
#               seq_num += 1

#           # Update how many filesize left to be read
#           filesize-= 32767

#         except socket.timeout:
#           # If ACK not received (packet loss, ack loss)
#           logging.info(f'Time out!')
#         except:
#           logging.info(f'Time out!')

    # s.close()