from pathlib import Path
import sys
import socket
import struct
import binascii

#sending port could be configurable based on context
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "0.0.0.0"
port = 8000
s.connect((host, port))

counter = 0

source_dir=Path('inputs/')
inputs = source_dir.iterdir()

def sync_input(inputs):
    for file_path in inputs:
        if file_path.is_file():
            print(f"--- Reading: {file_path.name} ---")
            with file_path.open('rb') as file_handle:
                for line in file_handle:
                    
                    chunk_bytes=line.rstrip()
                    if not chunk_bytes:
                        continue 
                        
                    global counter 
                    send_counter = counter.to_bytes(2, byteorder='big')                    
                    
                    checksum=binascii.crc_hqx(chunk_bytes, 0)
                    checksum_bytes = checksum.to_bytes(2, byteorder='big') 

                    body = send_counter + checksum_bytes + chunk_bytes
                    
                    total_len = len(body)
                    
                    header = struct.pack('>I', total_len)
                                        
                    print(f"Sending chunk # {counter}: checksum: {checksum}, {total_len} bytes")
                    
                    s.sendall(header + body)
                    
                    counter+=1
    s.close()    
                
def main():
    sync_input(inputs)
    
if __name__ == "__main__":
    main()
