import socket
import struct
from threading import *
import binascii

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "0.0.0.0"
port = 8000
serversocket.bind((host, port))
serversocket.listen(5)
servercounter = 0

print(f"Socket server listening on {host}:{port}")

def _recv_exactly(sock, num_bytes) -> bytearray | None:
    buffer = bytearray()
    while len(buffer) < num_bytes:
        try:
            data = sock.recv(num_bytes - len(buffer))
            if not data:
                return None
            buffer.extend(data)
        except (socket.error, ConnectionResetError):
             return None
    return buffer
    


class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()
        
    def run(self):
        while 1:
            global server_counter
            
            raw_len = _recv_exactly(self.sock, 4)
            if raw_len is None:
                print("Client disconnected")
                break
                
            msg_len = struct.unpack('>I', raw_len)[0]
            chunk = _recv_exactly(self.sock, msg_len)
            
            if chunk is None:
                print("Client disconnected mid send")
                break
            data = bytes(chunk)          
            
            counter_no = data[:2]
            raw_checksum = data[2:4]
            raw_chunk = data[4:]
            
            counter = int.from_bytes(counter_no, byteorder='big')
            recv_checksum = int.from_bytes(raw_checksum, byteorder='big')
            
            print(f"Received chunk # {counter}: checksum: {recv_checksum}")
            
            server_checksum=binascii.crc_hqx(raw_chunk, 0)
            server_checksum_bytes = server_checksum.to_bytes(2, byteorder='big') 
            
            if(server_checksum == recv_checksum):
                print(f"Chunk integrity validated")
            else:
                print(f"Chunk # {counter} corrupted - re-requesting")
                #send the chunk number back to client for reprocessing
                        
            
            
            ##in future, store recieved data in an index

            counter+=1
            
serversocket.listen(5)
print("Server listening")
while 1:
    clientsocket, address = serversocket.accept()
    client(clientsocket, address)
            