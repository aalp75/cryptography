# RSA  

## Contents
I – RSA  
II – Prime Numbers   
III – Code   
IV – How to Run    
V – Examples  

## I – RSA

This project implements the well-known **RSA cryptosystem**.

## II – Prime Numbers

The file `prime_number.py` contains basic number theory utilities related to prime numbers.

It includes:

- `pgcd` – Greatest Common Divisor  
- `is_prime` – Naive primality test  
- `is_prime_miller` – Miller–Rabin probabilistic primality test  
- Integer factorization:
  - Naive trial division  
  - Pollard’s Rho algorithm  

## III – Code

RSA is implemented as a class.

### Attributes

- `p` – First large prime number  
- `q` – Second large prime number  
- `n` – `p * q`  
- `phi` – `(p - 1) * (q - 1)`  
- `e` – Public exponent  
- `d` – Private exponent  

### Key Generation

- `e` is chosen as the first integer greater than `p` and `q` that is coprime with `phi`.
- `d` is computed as the modular inverse of `e` using the **Extended Euclidean Algorithm**.

You can test the robustness of your choice of `p` and `q` by applying **Pollard’s Rho factorization** to `n`, to evaluate how difficult it is to recover `p` and `q`.

## IV – How to Run

Create an RSA object:

```python
rsa = RSA(p, q)
```

If `p` or `q` are not prime numbers, an error message will be displayed.

Print the public and private keys:

```python
rsa.public_key()
rsa.private_key()
```

Write your plaintext in `message_clean.txt`.

To encrypt:

```python
rsa.encrypt_file('message_clean.txt')
```

The encrypted message will be saved in `message_encrypted.txt`.

To decrypt:

```python
rsa.decrypt_file('message_encrypted.txt')
```

The decrypted message will be written to `message_decrypted.txt`.

## V – Examples

```python
p = 379
q = 467
rsa = RSA(p, q)
```

```
RSA system created with success
Public Key :
(n,e) = (493,31)
Private Key :
(n,d) = (493,159)
```

For stronger security, it is recommended to choose `p` and `q` with at least 100 digits.

**Important:** 
You must ensure that `p * q > 9999` because the implementation groups numbers into blocks of 4 digits (`self.bloc = 4`) to reduce frequency analysis (you can modify this block size via `self.bloc`).

**message_clean.txt**

```
codeforces
```

**message_encrypted.txt**

```
['36381', '8869', '119216', '27023', '147686', '14299', '153430', '173375']
```
