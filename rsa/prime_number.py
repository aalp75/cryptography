import random
import numpy as np


def pgcd(a, b):
    if b == 0:
        return a
    r = a % b
    return pgcd(b, r)


# Deterministic method to determine if a number is prime
def is_prime(n):  # Naive method
    if n % 2 == 0:
        return False
    for i in range(3, int((np.sqrt(float(n))) + 2)):
        if n % i == 0:
            return False
    return True


def is_prime_faster(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i < n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i = i + 6
    return True


# Probabilistic method to determine if a number is prime

# Miller-Rabin primality test
def miller_test(d, n):
    a = 2 + random.randint(1, n - 4)
    x = pow(a, d, n)

    if x == 1 or x == n - 1:
        return True

    while d != n - 1:
        x = (x * x) % n
        d *= 2

        if x == 1:
            return False
        if x == n - 1:
            return True

    return False


def is_prime_miller(n, k):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True

    d = n - 1
    while d % 2 == 0:
        d //= 2

    for i in range(k):
        if miller_test(d, n) is False:
            return False

    return True


# Prime number factorization
def decomposition_prime_number(n):
    tmp = n
    res = []
    if n < 2:
        res.append(n)
        return res
    for i in range(2, n + 1):
        while n % i == 0:
            res.append(i)
            n /= i
    print(f"{tmp:d} = " + " * ".join(f"{item:d}" for item in res))
    return res


# Pollard Rho factorization
def facteursdiv2(n):
    """Factorization of n (integer) by trial division into two arbitrary factors"""
    pp = [2, 3, 5, 7, 11]
    racn = int(np.sqrt(n)) + 1  # integer square root of n
    for p in pp:
        if p > racn:
            return [n, 1]  # n is prime
        if n % p == 0:
            return [p, n // p] # a factorization has been found
    p = pp[-1] + 2
    while p <= racn:
        if n % p == 0:
            return [p, n // p] # a factorization has been found
        p += 2
    return [n, 1]


def pollardrho(n):
    """Factorization of a composite integer using Pollard's rho method"""
    f = lambda z: z * z + 1
    x, y, d = 2, 2, 1
    while d == 1:
        x = f(x) % n
        y = f(f(y)) % n
        d = pgcd(x - y, n)
    return [d, n // d]


def factpremiers(n):
    """List of prime factors of n, using recursive decomposition"""
    res = []  # list of prime factors found
    p = [n]  # computation stack
    while p != []:
        x = p.pop(-1)  # pop last stacked value
        if is_prime_miller(x, 1):
            res.append(x)  # a prime factor has been found → add it to the list
        else:
            a, b = pollardrho(x)  # compute a new decomposition
            if a == 1 or b == 1:
                a, b = facteursdiv2(x)  # fallback to trial division
            p.append(a)  # push a onto the stack
            p.append(b)  # push b onto the stack
    res.sort()
    print(f"{n:d} = " + " * ".join(f"{item:d}" for item in r))
    return res