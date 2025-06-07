# Replace this with your actual ciphertext (hex or bytes)
ciphertext_hex = b"3a21252a1e302c062a380006012a37102a27343b313a182a143b312a060013331c161c303b01390c2a193a1b32"
#ciphertext = bytes.fromhex(ciphertext_hex)

# Bruteforce all single-byte keys (0-255)
for key in range(256):
    key_bytes = bytes([key])
    decrypted = bytes([c ^ key_bytes[0] for c in ciphertext_hex])
    
    try:
        text = decrypted.decode()
        if "iotsec{" in text:
            print(f"[*] Found possible flag with key {key}: {text}")
            break
    except UnicodeDecodeError:
        continue

print("Bruteforce complete. No valid flag found with single-byte keys.")
