import random

# Return a k-bit random integer. If force_odd == True, the number will always be odd
def gen_random(k_bits: int, force_odd: bool=False) -> int:
    return 2**k_bits + random.randint(0, 2**(k_bits-1) - 1) | (1 if force_odd else 0)

# Test if odd number, n, is prime. Returns True if n is prime, with probability 1-(1/2)^k
def miller_rabin(n: int, k: int=100) -> bool:
    for _ in range(k):
        a = random.randint(1, n - 1)
        if expmod(a, n - 1, n) != 1:
            return False # definitely composite
    return True # probably true with probability > 1-(1/2)^k

# Modular exponentiation: (a^b) % m
def expmod(a: int, b: int, m: int) -> int:
    if b == 0:
        return 1
    result = 1
    while b > 0:
        if b % 2 == 1:
            result = (result * a) % m
        b //= 2
        a = (a * a) % m
    return result

# Return prime that passes k rounds of Miller-Rabin primality test
def gen_prime(k_bits: int, num_checks: int=100) -> int:
    n = gen_random(k_bits, force_odd=True)

    while not miller_rabin(n, num_checks):
        n = gen_random(k_bits, force_odd=True)

    return n

# Return prime of form 2q + 1, where q is prime
# https://en.wikipedia.org/wiki/Safe_and_Sophie_Germain_primes
def gen_safe_prime(k_bits: int, num_checks: int=100) -> int:
    q = gen_prime(k_bits - 1, num_checks)
    p = (2 * q) + 1

    while not miller_rabin(p, num_checks):
        q = gen_prime(k_bits - 1, num_checks)
        p = (2 * q) + 1

    return p

def extended_euclid(a: int, b: int) -> tuple[int, int, int]:
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        q = old_r // r # quotient of the division
        old_r, r = r, old_r - (q * r)
        old_s, s = s, old_s - (q * s)
        old_t, t = t, old_t - (q * t)

    # old_r = gcd(a, b)
    #       = old_s * a + old_t * b
    # GCD, Bezout coeff 1, Bezout coeff 2
    return old_r, old_s, old_t
