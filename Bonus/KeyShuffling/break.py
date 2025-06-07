def try_decrypt(enc_bytes):
    flag = [ord('S')]
    for i in range(len(enc_bytes) - 1):
        next_char = enc_bytes[i] ^ flag[-1]
        flag.append(next_char)
    # Close the cycle:
    if (flag[0] ^ flag[-1]) == enc_bytes[-1]:
        try:
            recovered = ''.join(chr(c) for c in flag)
            print(recovered)
        except:
            pass

# Read encrypted file
with open('iotsec_ctf1/Bonus/KeyShuffling/flagbonus.enc', 'rb') as f:
    enc_bytes = list(f.read())

flag = try_decrypt(enc_bytes)
print("Recovered flag:", flag if flag else "No valid flag found.")
