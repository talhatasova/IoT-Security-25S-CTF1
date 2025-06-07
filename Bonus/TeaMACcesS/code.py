import socket

HOST = '10.157.150.7'
PORT = 50008

def recv_until(s, prompt):
    data = b""
    while prompt.encode() not in data:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
    print(data.decode(), end='')
    return data.decode()


s = socket.socket()
s.connect((HOST, PORT))
initmsg = recv_until(s, 'Option')