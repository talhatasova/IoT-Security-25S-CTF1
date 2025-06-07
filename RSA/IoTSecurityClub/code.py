from Crypto.PublicKey import RSA

FLAG = "XXX"


def main():
    key = RSA.generate(1024)

    p, q, d, e, n = key.p, key.q, key.d, key.e, key.n

    print(f"[DEBUG]: e = {e:x}")
    print(f"[DEBUG]: n = {n:x}")

    print(
r"""
 _____           _____      ____   _____  ____   _   _   _____   _____   _____  __   __     ____   _      _   _   ____ 
/__ __\  _____  /__ __\    / ___\ /  __/ /  __\ / \ / \ / ___ \ /__ __\ /__ __\ \ \_/ /    /  __\ / \    / \ / \ /  _ \
  / \   / ___ \   / \      | |__  |  \   | /    | | | | | \_/ |   / \     / \    \_ _/     | /    | |    | | | | | | //
__\ /__ | \_/ |   | |      \___ | |  /_  | \__  | \_/ | |    /  __\ /__   | |     | |      | \__  | |_/\ | \_/ | | |_\\
\_____/ \_____/   \_/      \____/ \____\ \____/ \_____/ \_/\_\  \_____/   \_/     |_|      \____/ \____/ \_____/ \____/
                                                                                                                                                                                                                         
Welcome to the IoT Security Club!
To log in please provide a signature with the private key you received.
""")

    try:
        signature = int("2", 16)
        message = pow(signature, e, n)
        print(signature)
        print(message)

        if message == pow(signature, e, n) and message > 1 and signature > 1:
            print("Welcome")
            print(FLAG)
        else:
            print("Sorry mate")
    except:
        print("Computer is tired. Computer is going to sleep.")
        exit(1)


if __name__ == '__main__':
    main()
