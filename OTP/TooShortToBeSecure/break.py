def main():
    # ciphertext to hex
    cipher_hex = "3a21252a1e302c062a380006012a37102a27343b313a182a143b312a060013331c161c303b01390c2a193a1b32"
    cipher_bytes = bytes.fromhex(cipher_hex)

    for key in range(256):
        try:
            plaintext = ''.join(chr(b ^ key) for b in cipher_bytes)
            print(f"[Key={key:3} | Char='{chr(key)}'] -> {plaintext}")
        except UnicodeDecodeError:
            continue

if __name__ == "__main__":
    main()