import socket
from tqdm import tqdm
"""
I read that the RC4 stream cipher can be vulnerable to a bit-flipping attack, 
which would then also affect the security of my wireless LAN. 
I wonder if replacing RC4 with AES will solve the problem. 
Can you help me testing my proposed WLAN implementation, please?

iotsec
696F74736563
"""

HOST = '10.157.150.7'
PORT = 50007

def recv_until(s, prompt):
    data = b""
    while prompt.encode() not in data:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
    #print(data.decode(), end='')
    return data.decode()

def xor_hex_strings(hex1, hex2):
    return ''.join(f'{a ^ b:02x}' for a, b in zip(bytes.fromhex(hex1), bytes.fromhex(hex2)))

def main():
    plaintext = b"00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
    keystream = ""
    s = socket.socket()
    s.connect((HOST, PORT))
    initmsg = recv_until(s, 'Option')
    s.sendall(b'2\n')
    recv_until(s, 'hex')
    s.sendall(plaintext)
    initmsg = recv_until(s, 'Option')
    response = initmsg.split("\n")
    ref_keystream = response[0].strip()
    s.sendall(b'2\n')
    recv_until(s, 'hex')
    s.sendall(plaintext)
    initmsg = recv_until(s, 'Option')
    response = initmsg.split("\n")
    ref2_keystream = response[0].strip()

    isRepeated = False
    while not isRepeated:
        s.sendall(b'2\n')
        recv_until(s, 'hex')
        s.sendall(plaintext)
        initmsg = recv_until(s, 'Option')
        keystream = initmsg.split("\n")[0].strip()
        isRepeated = ref_keystream == keystream
        print(f"{ref_keystream=}\t{keystream=}")

    s.sendall(b'1\n')
    encrypted_packet_response = recv_until(s, 'Option')
    encrypted_packet = encrypted_packet_response.split("\n")[0].strip()
    flag_hex = xor_hex_strings(ref2_keystream, encrypted_packet)
    try:
        flag_ascii = bytes.fromhex(flag_hex).decode()
        print(f"Flag (ASCII): {flag_ascii}")
    except Exception as e:
        print(f"Flag (hex): {flag_hex}")


if __name__ == "__main__":
    main()
