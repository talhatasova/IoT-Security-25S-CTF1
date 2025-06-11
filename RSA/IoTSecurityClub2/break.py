import re
import socket
from Crypto.Util.number import getRandomNBitInteger, inverse, long_to_bytes

HOST = '10.157.150.7'
PORT = 50004

# === Connect and get public key ===
s = socket.socket()
s.connect((HOST, PORT))

# === Get the challenge from Login ===
def get_menu():
    menu = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        menu += chunk
        if b"Option:" in menu:
            break
    return menu.decode()

public_key = get_menu()
#print(public_key)
e = int(re.search(r"e\s*=\s*0x([0-9a-fA-F]+)", public_key).group(1), 16)
n = int(re.search(r"n\s*=\s*0x([0-9a-fA-F]+)", public_key).group(1), 16)

# Send option 1 for login
s.sendall(b'1\n')

response = s.recv(4096).decode()
print(response)

challenge_line = [line for line in response.splitlines() if "challenge" in line.lower()][0]
challenge_hex = challenge_line.split(":")[-1].strip()
challenge = int(challenge_hex, 16)
s.sendall(b'11111111\n')
response = s.recv(4096).decode()
print(response)

# === Helper: Get signature from chat ===
def get_signature(msg_bytes):
    #print(get_menu())
    get_menu()
    s.sendall(b'2\n')
    response = s.recv(4096).decode()
    print(response)
    s.sendall(msg_bytes.hex().encode() + b'\n')
    response = s.recv(4096).decode()
    print(response)
    if "#" not in response:
        return None
    parts = response.strip().split('\n')
    return int(parts[0].split("#")[1].strip(), 16)

# === Find m1, m2 such that m1 * m2 == challenge mod n ===
while True:
    m1 = getRandomNBitInteger(128)
    m1_bytes = long_to_bytes(m1)
    if b'challenge_' in m1_bytes.lower():
        continue
    sig1 = get_signature(m1_bytes)
    if sig1 is None:
        continue

    try:
        m2 = (challenge * inverse(m1, n)) % n
        m2_bytes = long_to_bytes(m2)
        if b'challenge_' in m2_bytes.lower():
            continue
        sig2 = get_signature(m2_bytes)
        if sig2 is None:
            continue
        print("[+] Found m1, m2!")
        break
    except:
        continue

# === Build the final signature ===
final_sig = (sig1 * sig2) % n
print("[+] Final Signature:", hex(final_sig))

# === Submit forged signature in login ===
response = s.recv(4096).decode()
print(response)
s.sendall(b'1\n')
response = s.recv(4096).decode()
print(response)
s.sendall(hex(final_sig).encode() + b'\n')

# === Get flag ===
response = s.recv(4096).decode()
print(response)
