from util import gen_safe_prime, expmod, extended_euclid
import random
import math

class ElGamal:
    def __init__(self, k: int = 1000, public_keys: tuple[int] = None, a: int = None, num_checks: int = 100):
        if not public_keys:
            self.p = gen_safe_prime(k, num_checks=num_checks)
            self.g = self.get_generator()
            self.a = random.randint(0, self.p - 1)
            self.b = expmod(self.g, self.a, self.p)
        else:
            self.p, self.g, self.b = public_keys
            self.a = a if a else random.randint(0, self.p - 1)
        self.k = math.floor(math.log2(self.p))

    @property
    def pub_keys(self):
        return self.p, self.g, self.b

    @property
    def private_key(self):
        return self.a

    def get_generator(self) -> int:
        q = (self.p - 1) // 2
        n = random.randint(2, self.p - 1)
        while (n*n) % self.p == 1 or expmod(n, q, self.p) == 1:
            n = random.randint(2, self.p - 1)
        return n

    def encrypt(self, x: int) -> tuple[int, int]:
        alpha = random.randint(0, self.p - 1)
        beta = expmod(self.g, alpha, self.p)
        f = expmod(self.b, alpha, self.p)
        x = (x * f) % self.p

        return x, beta

    def decrypt(self, x: int, beta: int) -> int:
        f = expmod(beta, self.a, self.p)
        _, f_inv, _ = extended_euclid(f, self.p)

        x = (x * f_inv) % self.p
        return x

    def encrypt_text(self, text: str) -> list[tuple[int, int]]:
        bytes = text.encode('utf-8') # byte string representing text
        bytes_per_n = max(self.k // 8, 1)

        # split text into chunks of k bits and convert them to integers
        ints = []
        for i in range(math.ceil(len(bytes) / bytes_per_n)):
            byte_substr = bytes[i*bytes_per_n : (i+1)*bytes_per_n]
            ints.append(int(byte_substr.hex(), base=16))

        # encrypt the integer representation of text
        return [self.encrypt(i) for i in ints]

    def decrypt_text(self, cypher: list[tuple[int, int]]) -> str:
        text = ''

        for (x, beta) in cypher:
            m = self.decrypt(x, beta)
            num_bytes = 1 if m == 1 else math.ceil(math.log(x)/math.log(256))
            text += m.to_bytes(num_bytes, 'big').decode('utf-8')

        return text
