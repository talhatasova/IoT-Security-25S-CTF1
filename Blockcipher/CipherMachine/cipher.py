import socket

def recv_until(sock, prompt):
    """Receive data until the prompt is found."""
    data = b""
    while prompt.encode() not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data.decode()

# Connect to the server
HOST = '10.157.150.7'
PORT = 50002
s = socket.socket()
s.connect((HOST, PORT))

# Step 1: Receive initial prompt
initial_response = recv_until(s, "Option:")
session_id = initial_response.split("ID = ")[1].split("\n")[0].strip()

# Step 2: Send option 1 (encrypt a 0-filled packet of the same length as session_id)
s.sendall(b'1\n')
recv_until(s, "(hex)")

# Send zero-packet with same length (in bytes)
input_packet = '00' * (len(session_id) // 2)
s.sendall(input_packet.encode() + b'\n')

# Step 3: Receive the encrypted response
encryption_result = recv_until(s, "Option:")
encrypted_packet = encryption_result.strip().split("Response: ")[1].split("\n")[0].strip()

# Step 4: Decrypt the session_id in 3 parts
decrypt = ""
session_id_bytes = bytes.fromhex(session_id)
part_size = len(session_id_bytes) // 3

for i in range(3):
    part = session_id_bytes[i*part_size:(i+1)*part_size]
    s.sendall(b'2\n')
    recv_until(s, "(hex)")
    s.sendall(part.hex().encode() + b'\n')
    response = recv_until(s, "Option:")
    decrypted_part = response.strip().split("Response: ")[1].split("\n")[0].strip()
    decrypt += decrypted_part

print("Decrypted session ID (hex):", decrypt)
ascii_output = bytes.fromhex(decrypt).decode('utf-8', errors='replace')
print("Decrypted session ID (ASCII):", ascii_output)

# ECB Mode causes problems here. repeating patterns in the ciphertext. send 00 and find its decrypted text. then, decrypt the session id block by block.
# Receive the encrypted packet

#732e60fac150a79c581fd652d7d0379b
#00000000000000000000000000000000 00000000000000000000000000000000 00000000000000000000000000000001

#d171b42124da57d588e52671befcdbf0 6db9a54c3508cb701a8a75ebd773f5df 8920479d5d960b7e7ade2b3e3b92d726
#696f747365637b4563425f4d6f64455f 6361555365535f4d414e795f50724f62 6c654d537d0b0b0b0b0b0b0b0b0b0b0b
#04045481163e90d4cc0417f1d4e26caf 4a505656d9576ae54870da572cc61a2c 89d3f21193aefc1ef5a901d5fbb96e3b