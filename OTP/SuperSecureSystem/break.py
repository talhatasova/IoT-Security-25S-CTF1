import socket

def xor_bytes(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

HOST = '10.157.150.7'
PORT = 50006

with socket.create_connection((HOST, PORT)) as s:
    def recv_until(prompt):
        data = b""
        while not data.endswith(prompt):
            data += s.recv(1)
        return data


    print(s.recv(1024).decode())


    # Step 1: Send known  plaintext

    known_plain = b"A" * 32  # Length matches SHA-256 output

    s.sendall(b"2\n")
    recv_until(b"challenge: ")
    s.sendall(known_plain + b"\n")

    line = s.recv(1024).decode()
    encrypted_known = bytes.fromhex(line.strip().split(": ")[1])
    print("[+] Encrypted known:", encrypted_known.hex())

    # Recover key
    key = xor_bytes(known_plain, encrypted_known)
    print("[+] Recovered key:", key.hex())


    # Step 2: Get encrypted flag

    s.sendall(b"1\n")


    while True:
        line = s.recv(1024).decode()
        if "encrypted_flag: " in line:
            encrypted_flag_hex = line.strip().split(": ")[1]
            break
        else:
            print("Skipping line:", line.strip())

    encrypted_flag = bytes.fromhex(encrypted_flag_hex)
    print("[+] Encrypted flag:", encrypted_flag.hex())

    # Decrypt flag
    decrypted_flag = xor_bytes(encrypted_flag, key[:len(encrypted_flag)])
    print("[+] Decrypted flag:", decrypted_flag.decode())
