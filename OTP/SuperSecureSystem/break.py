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

    known_plain = b"A" * 32
    s.sendall(b"2\n")
    init_msg = recv_until(b"challenge: ")
    print(init_msg.decode())
    s.sendall(known_plain + b"\n")

    line = s.recv(1024).decode()
    print(line)
    encrypted_known = bytes.fromhex(line.strip().split(": ")[1])

    # Recover key
    key = xor_bytes(known_plain, encrypted_known)
    print("[+] Recovered key:", key.hex())


    # Step 2: Get encrypted flag

    s.sendall(b"1\n")

    line = recv_until(b"encrypted_flag: ")
    line += s.recv(4096)
    encrypted_flag_hex = line.decode().strip().split(": ")[-1]

    encrypted_flag = bytes.fromhex(encrypted_flag_hex)
    print("[+] Encrypted flag:", encrypted_flag.hex())

    # Decrypt flag
    decrypted_flag = xor_bytes(encrypted_flag, key[:len(encrypted_flag)])
    print("[+] Decrypted flag:", decrypted_flag.decode())
