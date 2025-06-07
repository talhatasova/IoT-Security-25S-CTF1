import socket
import base64

HOST = '10.157.150.7'
PORT = 50010

def recv_until(s, prompt):
    data = b""
    while prompt.encode() not in data:
        data += s.recv(4096)
    return data.decode()

s = socket.socket()
s.connect((HOST, PORT))

# Get banner
recv_until(s, "Enter your choice:")

# Send 1 for challenge
s.sendall(b'1\n')
response = recv_until(s, "Enter your choice:")
print(response)

# Extract challenge
challenge_line = [line for line in response.splitlines() if line.startswith("Challenge")][0]
challenge_b64 = challenge_line.split(": ")[1]
decoded = base64.b64decode(challenge_b64).decode()
print("[+] Decoded Challenge:", decoded)

# Send 2 for solution
s.sendall(b'2\n')
recv_until(s, "Give me your solution:")
s.sendall(decoded.encode() + b'\n')

# Get result
result = s.recv(4096).decode()
print(result)
