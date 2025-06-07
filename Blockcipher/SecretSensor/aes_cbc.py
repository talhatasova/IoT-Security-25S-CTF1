from Crypto.Cipher import AES
import re

def unpad(data):
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 16:
        raise ValueError("Invalid padding.")
    return data[:-pad_len].decode()

# --- AES-CBC Decrypt Function ---
def aes_cbc_decrypt(ciphertext, key, iv):
    aes = AES.new(key, AES.MODE_CBC, iv)
    plaintext = aes.decrypt(ciphertext)
    return plaintext

def aes_ecb_decrypt_block(block, key):
    aes = AES.new(key, AES.MODE_ECB)
    return aes.decrypt(block)


temp_enc_file = "/home/talhatasova/iotsec_ctf1/Blockcipher/SecretSensor/temp_readings.enc"
secret_enc_file = "/home/talhatasova/iotsec_ctf1/Blockcipher/SecretSensor/secret_readings.enc"
key_hex = "20e2a92c496b2fceb5d6bda6e2141351"
key = bytes.fromhex(key_hex)

# --- Load Encrypted Files ---
with open(temp_enc_file, "rb") as f:
    temp_cipher = f.read()

    temp_second_block = temp_cipher[(1)*16:(2)*16]
    decrypted_second_mid_block = aes_ecb_decrypt_block(temp_second_block, key)

    temp_first_block = temp_cipher[(0)*16:1*16]
    decrypted_first_mid_block = aes_ecb_decrypt_block(temp_first_block, key)

    plaintext = bytes(a ^ b for a, b in zip(decrypted_second_mid_block, temp_first_block))
    iv = bytes(a ^ b for a, b in zip(decrypted_first_mid_block, plaintext))
    
    print(f"Decrypted Text: {unpad(plaintext)}")
    print(f"IV: {iv.hex()}")


with open(secret_enc_file, "rb") as f:
    secret_cipher = f.read()

    secret_decrypted = aes_cbc_decrypt(secret_cipher, key, iv)
    print(f"Secret Decrypted: {secret_decrypted}")
