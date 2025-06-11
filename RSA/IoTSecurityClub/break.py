from Crypto.Util.number import long_to_bytes
import socket

HOST = '10.157.150.7'
PORT = 50003

def recv_until(sock, prompt):
    data = b""
    while prompt.encode() not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data.decode()

# Connect to the server
s = socket.socket()
s.connect((HOST, PORT))
initmsg = recv_until(s, "Message (hex)")
e_debug, n_debug = initmsg.split("\n")[0:2]
e_str = e_debug[e_debug.index("e =") + 6:]
n_str = n_debug[n_debug.index("n =") + 6:]

# Given RSA parameters
e = int(e_str, 16)
n = int(n_str, 16)

# Pick the signature as 2 from code.py
signature = int("2", 16)

# Compute message = signature^e mod n
message = pow(signature, e, n)
s.sendall(hex(message).encode() + b'\n')
recv_until(s, "Signature (hex)")
s.sendall(str(signature).encode() + b'\n')

response = s.recv(4096).decode()
print(response)
