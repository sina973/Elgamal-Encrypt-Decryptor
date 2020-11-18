import subprocess


def import_or_install(package):
    try:
        return __import__(package)
    except ImportError:
        subprocess.check_call(["python", "-m", "pip", "install", package])


random = import_or_install("random")
sympy = import_or_install("sympy")  # for checking prime
np = import_or_install("numpy")


class Elgamal(object):
    def __init__(self):
        self.pukey = None
        self.prkey = None
        self.q = None
        self.g = None
        self.p = None
        self.message = None
        self.C1 = None
        self.C2 = None
        self.saving_path = None

    def set_private_key(self, k):
        self.prkey = k

    def set_public_key(self, k):
        self.pukey = k

    def gen_keys(self):
        p = 0
        q = 0
        g = 0
        while not sympy.isprime(p):
            q = 0
            while not sympy.isprime(q):
                q = random.randint(pow(2, 63), pow(2, 64))

            p = 2 * q + 1  # find a prime number q so that 2*q+1 = p (p is prime). this is done to finding g easier.

        while (pow(g, q, p) != 1) and (pow(g, 2) != 1):
            g = random.randint(2, p)

        a = random.randint(2, q)  # private key
        h = pow(g, a, p)  # public key g^a mod p

        print("p = ", p)
        print("q = ", q)
        print("p is prime: ", sympy.isprime(p))
        print("q is prime: ", sympy.isprime(q))
        print("g = ", g)
        print("g^q mod p = ", pow(g, q, p))
        print("public key is: ", h)
        print("private key is: ", a)
        pqg = str(p) + "," + str(q) + "," + str(g)

        f = open(self.saving_path + "/public_key.txt", "w+")
        f.write(str(h))  # public_key.txt
        f.close()
        f = open(self.saving_path + "/private_key.txt", "w+")
        f.write(str(a))  # private_key.txt
        f.close()
        f = open(self.saving_path + "/pqg.txt", "w+")
        f.write(str(pqg))  # pqg_key.txt
        f.close()

    # Asymmetric encryption

    def encrypt(self):

        c2 = []

        r = random.randint(2, self.q)
        s = pow(self.pukey, r, self.p)  # h^r mod p
        c1 = pow(self.g, r, self.p)

        for i in range(0, len(self.message)):
            c2.append(self.message[i])  # convert characters of string message to array of
                                        # characters which each element is a character.
        c2 = np.array(c2)  # make a numpy for more efficient computation.
        c2 = self.array_en_sub(
            c2)  # substitution of character with it's integer number, according to table of substitution
        c2 = c2 * s  # multiply each character by s. to encrypt

        encrypted_message = ",".join(str(element) for element in c2)
        txt = str(c1) + "\n" + str(encrypted_message)
        f = open(self.saving_path + "/Encrypted_Message.txt", "w+")
        f.write(str(txt))  # Encrypted_Message.txt
        f.close()

    def decrypt(self):
        message_list = self.message.split("\n")
        self.C1 = int(message_list[0])  # c1, private_key, p, is needed to find the decryption scalar.
        message = message_list[1].split(",")
        message = np.array(message, dtype=np.float64)

        c1_a = pow(self.C1, self.prkey,
                   self.p)  # (c1^a mod p). C1 = g^r (r is used to encrypt the message(h^r). h = g^a, a is private key. ==> [message * h^r / g^(r*a)] = message * (g^a)^r / g^(r*a) = message

        np_array = np.true_divide(message, c1_a)
        message = self.array_de_sub(np_array)  # substitution of integer and character

        decrypted_message = "".join(str(element) for element in message)
        f = open(self.saving_path + "/Decrypted_Message.txt", "w+")
        f.write(str(decrypted_message))  # Decrypted_Message.txt
        f.close()

        # return dr_msg

    def array_en_sub(self, x):
        return np.array([self.en_sub(xi) for xi in x], dtype=np.float64)

    def array_de_sub(self, x):
        return np.array([self.de_sub(int(round(xi))) for xi in x])

    # Substitution tables:

    def en_sub(self, msg):
        msg = str.lower(msg)
        if msg == " ":
            msg = 54  # in Elgamal message characters multiply by a scaler to find an encrypt character. So encryption of 0 is 0. due to the safety of encryption we decide to use a non-zero integer for substitution of space character.
        elif 48 <= ord(msg) <= 57:
            msg = ord(msg) - 21
        elif 97 <= ord(msg) <= 122:
            msg = ord(msg) - 96
        elif msg == ".":
            msg = 37
        elif msg == "?":
            msg = 38
        elif msg == ",":
            msg = 39
        else:
            msg = int(ord(msg) + 41)
        '''elif msg == "-":
            msg = 40
        elif msg == "\n":
            msg = 41
        elif msg == "\r":
            msg = 42
        elif msg == "'":
            msg = 43
        elif msg == "\"":
            msg = 44
        elif msg == "!":
            msg = 45
        elif msg == "]":
            msg = 46
        elif msg == "[":
            msg = 47
        elif msg == "+":
            msg = 48
        elif msg == "=":
            msg = 49
        elif msg == "(":
            msg = 50
        elif msg == ")":
            msg = 51
        elif msg == ";":
            msg = 52
        elif msg == ":":
            msg = 53'''

        return int(msg)

    def de_sub(self, msg):
        if msg == 54:
            msg = " "
        elif 27 <= msg <= 36:
            msg = chr(msg + 21)
        elif 1 <= msg <= 26:
            msg = chr(msg + 96)
        elif msg == 37:
            msg = "."
        elif msg == 38:
            msg = "?"
        elif msg == 39:
            msg = ","
        elif msg == 40:
            msg = "-"
        else:
            msg = chr(msg - 41)

        '''elif msg == 41:
            msg = "\n"
        elif msg == 42:
            msg = "\r"
        elif msg == 43:
            msg = "'"
        elif msg == 44:
            msg = "\""
        elif msg == 45:
            msg = "!"
        elif msg == 46:
            msg = "]"
        elif msg == 47:
            msg = "["
        elif msg == 48:
            msg = "+"
        elif msg == 49:
            msg = "="
        elif msg == 50:
            msg = "("
        elif msg == 51:
            msg = ")"
        elif msg == 52:
            msg = ";"
        elif msg == 53:
            msg = ":"'''

        return str(msg)
