import socket

# Connect to the server
HOST = '10.157.150.7'
PORT = 50002
s = socket.socket()
s.connect((HOST, PORT))

def recv_until(s, prompt):
    data = b""
    while prompt.encode() not in data:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
    return data.decode()


def send_and_recv(s, data):
    s.sendall(data + b'\n')
    response = s.recv(4096).decode()
    print("[+] Server response:", response.strip())
    return response

# Receive initial prompt
initial_response = recv_until(s, "Option:")
session_id = initial_response.split("ID = ")[1].strip().split("\n")[0]
print("[+] Initial response from server:", initial_response.strip())

# Send option 1 to get the encrypted packet
send_and_recv(s, b'1')
input_packet = b'00' * (len(session_id) // 2)
encryption_result = send_and_recv(s, input_packet)
encrypted_packet = encryption_result.strip().split("Response: ")[1].strip()

# ECB Mode causes problems here. repeating patterns in the ciphertext. send 00 and find its decrypted text. then, decrypt the session id block by block.
# Receive the encrypted packet

#732e60fac150a79c581fd652d7d0379b
#00000000000000000000000000000000 00000000000000000000000000000000 00000000000000000000000000000001

#d171b42124da57d588e52671befcdbf0 6db9a54c3508cb701a8a75ebd773f5df 8920479d5d960b7e7ade2b3e3b92d726
#696f747365637b4563425f4d6f64455f 6361555365535f4d414e795f50724f62 6c654d537d0b0b0b0b0b0b0b0b0b0b0b