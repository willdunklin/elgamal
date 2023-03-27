from util.encryption import Encryption
from util.util import gen_safe_prime, expmod, mul_inv
import random
import math

class ElGamal(Encryption):
    def __init__(self, k: int = 1000, public_keys: tuple[int] = None, priv_key: int = None, num_checks: int = 100):
        if not public_keys:
            self.p = gen_safe_prime(k, num_checks=num_checks)
            self.g = self.get_generator()
            self.a = random.randint(0, self.p - 1)
            self.b = expmod(self.g, self.a, self.p)
        else:
            self.p, self.g, self.b = public_keys
            self.a = priv_key if priv_key else random.randint(0, self.p - 1)
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
        return (x * mul_inv(f, self.p)) % self.p

    def decrypt_text(self, cypher: list[tuple[int, int]]) -> str:
        cypher = [(c[1], c[0]) for c in cypher] # have to reverse the order of tuples for it to work
        return super().decrypt_text(cypher)
