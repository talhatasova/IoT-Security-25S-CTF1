import socket

HOST = '10.157.150.7'
PORT = 50005

BLOCK_SIZE = 16  # AES block size

def get_blocks(ciphertext_hex):
    return [ciphertext_hex[i:i+BLOCK_SIZE*2] for i in range(0, len(ciphertext_hex), BLOCK_SIZE*2)]

def send_and_recv(s, data):
    s.sendall(data + b'\n')
    response = s.recv(4096).decode()
    return response

# Connect to server
s = socket.socket()
s.connect((HOST, PORT))
initmsg = s.recv(4096)

if "Ciphertext" not in initmsg.decode():
    initmsg += s.recv(4096)

# Parse IV and ciphertext
keywords = initmsg.decode().split("\n")
iv = keywords[-4].split("=")[-1].strip()
ciphertext = keywords[-3].split("=")[-1].strip()

print(f"IV: {iv}")
print(f"Ciphertext: {ciphertext}")

# Setup blocks
blocks = [iv] + get_blocks(ciphertext)
plaintext = b''

# Padding Oracle Attack
for block_index in range(len(blocks) - 1, 0, -1):
    print(f"\nDecrypting block {block_index}/{len(blocks)-1}...")
    known_bytes = bytearray(BLOCK_SIZE)
    prev_block = bytearray.fromhex(blocks[block_index - 1])
    target_block = blocks[block_index]

    for byte_pos in range(1, BLOCK_SIZE + 1):
        pad_byte = byte_pos
        for guess in range(256):
            # Build modified previous block
            modified_block = prev_block[:]
            for k in range(1, byte_pos):
                modified_block[-k] ^= known_bytes[-k] ^ pad_byte
            modified_block[-byte_pos] ^= guess ^ pad_byte

            test_cipher = bytes.fromhex(target_block)
            test_message = modified_block.hex() + target_block
            response = send_and_recv(s, test_message.encode())

            if "Incorrect padding" not in response:
                print(f"Found byte: {guess:02x}")
                known_bytes[-byte_pos] = guess
                break

    decrypted_block = bytes(known_bytes)
    plaintext = decrypted_block + plaintext
    print(f"Decrypted block plaintext: {decrypted_block}")

print("\nFinal plaintext:")
print(plaintext)
print(plaintext.decode(errors='ignore'))
