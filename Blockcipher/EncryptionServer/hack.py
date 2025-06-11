import socket

HOST = '10.157.150.7'
PORT = 50001

"""
Hey, check out my new encryption server. 
It takes your message, appends an additional secret and encrypts the entire string. 
In my opinion, this is unbreakable. 
If you doubt it, just prove me wrong by submitting the secret in the form: iotsec{secret}
"""

def send_and_recv(s, data):
    s.sendall(data + b'\n')
    response = s.recv(4096).decode()
    #print(response[:32])
    return response

# Connect to the server
s = socket.socket()
s.connect((HOST, PORT))
initmsg = s.recv(4096)
print(initmsg.decode())


ref = "000102030405060708090A0B0C0D0E"  # Initial reference message
secret = "6543625F4D4F44655F69735F4E4F545F7345635572"
secret = ""

ref_response = send_and_recv(s, (ref+secret).encode())[:32]

while len(secret) < 32:
    for i in range(255):
        message = f"{ref}{secret}{i.to_bytes(1).hex()}"
        response = send_and_recv(s, message.encode())
        if response[:32] == ref_response:
            print(f"Found secret byte: {i.to_bytes(1).hex()}")
            secret = secret + i.to_bytes(1).hex()
            ref = ref[:30-len(secret)]  # Adjust ref to match the new secret length
            ref_response = send_and_recv(s, ref.encode())[:32]
            break
    
print(f"Secret found: {bytes.fromhex(secret).decode()}")

""" 000102030405060708090A0B0C0D0E0F 000102030405060708XXXXXXXXXXXXXX
6b03a7ef4da6526133837818218d76d0 65a811fca7e208f68a22b760103fb397c42794c7b974207fbb6162fe2df9ba5f
000102030405060708090A0B0C0D0E0F 000102030405060708090A0B0C0D0E0F 000102030405060708                  
6b03a7ef4da6526133837818218d76d0 6b03a7ef4da6526133837818218d76d0 65a811fca7e208f68a22b760103fb397c42794c7b974207fbb6162fe2df9ba5f

000102030405060708090A0B0C0D0EXX XXXXXXXXXXXXPPPPPPPPPPPPPPPPPPPP
c731621241cdd6e1d79f133d7aaeb02d adac73512af12f1ad925c2fbb5a5f356 a37c7d5f1dfd96972ca8277c5e6b6280 """
""" eCb_MODe_is_NOT_sEcUre """

# adac73512af12f1ad925c2fbb5a5f356

