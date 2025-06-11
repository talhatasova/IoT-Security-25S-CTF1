import socket
import base64
import string
from itertools import cycle

HOST = '10.157.150.7'
PORT = 50009

def recv_until(s, prompt):
    data = b""
    while prompt.encode() not in data:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
    print(data.decode(), end='')
    return data.decode()

def caesar_cipher(text, offset):
    shifted = ""
    for c in text:
        if c.isupper():
            shifted += chr((ord(c) - ord('A') + offset) % 26 + ord('A'))
        elif c.islower():
            shifted += chr((ord(c) - ord('a') + offset) % 26 + ord('a'))
        else:
            shifted += c
    return shifted

def main():
    s = socket.socket()
    s.connect((HOST, PORT))

    recv_until(s, "Enter your choice:")

    # Send '1' to get the challenge
    s.sendall(b'1\n')
    response = recv_until(s, "Enter your choice:")

    # Extract the challenge
    for line in response.splitlines():
        if line.startswith("Challenge:"):
            challenge_b64 = line.split(": ")[1]
            print("Challenge found:", challenge_b64)
            break
    else:
        print("Challenge not found.")
        return

    for offset in range(26):
        shifted = caesar_cipher(challenge_b64, offset)
        print(f"Offset {offset}: {shifted}")
        s.sendall(b'2\n')
        recv_until(s, "Give me your decrypted text:")
        s.sendall(bytes(shifted.encode()) + b'\n')
        response = recv_until(s, "Enter your choice:")
    s.close()

if __name__ == "__main__":
    main()
