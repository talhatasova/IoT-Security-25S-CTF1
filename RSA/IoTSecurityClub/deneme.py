from Crypto.Util.number import long_to_bytes

# Given RSA parameters
e = 0x10001
n = int("c489f0c51179fbf7b5619d4560e3b401f177bba93acb05110018dbe090fa7ebbe3351ca21862d93f50c5cfba90790a37e0b545494be047e4218865c2347568ba568f859a0ff5ecc1ec30134aa78440d9029166a50da4d9e3495281137e6785a846e89390c0ddd3aff45f48875065de4efcdfdb1183b13cd653a9dabeddae199d", 16)

# Pick a signature
signature = 2

# Compute message = signature^e mod n
message = pow(signature, e, n)

print("Signature (hex):", hex(signature)[2:])
print("Message (hex):", hex(message)[2:])
