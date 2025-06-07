from Crypto.PublicKey import RSA
import base64
import os

FLAG = "XXX"

challenge = int.from_bytes(f"challenge_{os.urandom(8).hex()}".encode(), 'big')

def menu():
    print(
        r"""
[1] Login
[2] Support
[3] Exit
        """
    )
    return int(input("Option:"))

def int_to_bytes(i):
    return i.to_bytes((i.bit_length() + 7) // 8, 'big')

def chat():
    message = int(input("Message:"), 16)

    if b"challenge_" in int_to_bytes(message).lower():
        print("This message looks like a challenge")
    else:
        # TODO: Implement actual chat. Currently it's just a dummy.
        answer = message # put actual answer here
        signature = pow(answer, d, n)
        print(f"{message:x}#{signature:x}")

def login():
    print(f"Provide a valid signature for the following challenge: {challenge:x}")
    signature = int(input("Signature:"), 16)

    if challenge == pow(signature, e, n) and challenge > 1 and signature > 1:
        print("Welcome")
        print(FLAG)
    else:
        print("Sorry mate")

def main():
    global p, q, d, e, n
    key = RSA.generate(1024)

    p, q, d, e, n = key.p, key.q, key.d, key.e, key.n

    print(f"[DEBUG]: e={e:x}")
    print(f"[DEBUG]: n={n:x}")

    print(
    r"""
 _____           _____      ____   _____  ____   _   _   _____   _____   _____  __   __     ____   _      _   _   ____ 
/__ __\  _____  /__ __\    / ___\ /  __/ /  __\ / \ / \ / ___ \ /__ __\ /__ __\ \ \_/ /    /  __\ / \    / \ / \ /  _ \
  / \   / ___ \   / \      | |__  |  \   | /    | | | | | \_/ |   / \     / \    \_ _/     | /    | |    | | | | | | //
__\ /__ | \_/ |   | |      \___ | |  /_  | \__  | \_/ | |    /  __\ /__   | |     | |      | \__  | |_/\ | \_/ | | |_\\
\_____/ \_____/   \_/      \____/ \____\ \____/ \_____/ \_/\_\  \_____/   \_/     |_|      \____/ \____/ \_____/ \____/
                                                                                                                                                                                                                         
Welcome to the IoT Security Club!
To log in please provide a signature with the private key you received.

We had some issues with the login system and changed the procedure. 
If you have problems with the new process please ask our support team (of course all messages are signed by the support team, so you know it's us).
""")

    try:
        while True:
            option = menu()
            print()

            if option == 1:
                login()
            elif option == 2:
                chat()
            else:
                exit(0)
    except SystemExit:
        pass
    except:
        print("Computer is tired. Computer is going to sleep.")
        exit(1)


if __name__ == '__main__':
    main()