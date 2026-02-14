import json
import os
from prime_number import *
from utils import *

class RSA:
    def __init__(self, p, q):
        cond = True
        if is_prime_miller(p, 1000) is False:
            print('\033[1m' + 'ERROR \n' + '\033[0m' + f'{p} is not a prime number')
            cond = False
        if is_prime_miller(q, 1000) is False:
            print('\033[1m' + 'ERROR \n' + '\033[0m' + f'{q} is not a prime number')
            cond = False

        self.p = p
        self.q = q
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        self.e = find_key(p, q)
        _, _, self.d = extended_euclidean(self.phi, self.e)
        self.bloc = 4

        if cond:
            print('RSA system created with success')

    def public_key(self):
        print(
            '\033[1m'
            + 'Public Key :'
            + '\033[0m'
            + f'\n(n,e) = ({self.n},{self.e})'
        )

    def private_key(self):
        print(
            '\033[1m'
            + 'Private Key :'
            + '\033[0m'
            + f'\n(n,d) = ({self.n},{self.d})'
        )

    def encrypt(self, m):
        return pow(m, self.e, self.n)

    def decrypt(self, c):
        return pow(c, self.d, self.n)

    def encrypt_list(self, l):
        res = []
        for elmt in l:
            res.append(self.encrypt(elmt))
        return res

    def decrypt_list(self, l):
        res = []
        for elmt in l:
            res.append(self.decrypt(elmt))
        return res

    def encrypt_text(self, sentence):
        list_tmp = []

        for char in sentence:
            list_tmp.append(str(ord(char)))
        list_tmp = complete_with_0(list_tmp, 3)

        list_tmp = bloc_s1_to_s2(list_tmp, 3, self.bloc)

        list_res = [int(st) for st in list_tmp]

        list_res = self.encrypt_list(list_res)

        res = [str(i) for i in list_res]
        return res

    def decrypt_text(self, sentence):
        tmp = [int(i) for i in sentence]

        tmp = self.decrypt_list(tmp)

        tmp2 = complete_with_0([str(i) for i in tmp], self.bloc)

        tmp = bloc_s1_to_s2(tmp2, self.bloc, 3)

        res = ''
        for ind in tmp:
            res = res + chr(int(ind))
        return res

    def encrypt_file(self, pathfile):

        base_dir = os.path.dirname(os.path.abspath(__file__))

        clean_path = os.path.join(base_dir, pathfile)
        encrypt_path = os.path.join(base_dir, 'message_encrypted.txt')

        with open(clean_path, 'r') as myfile:
            contents = myfile.read()
        res = self.encrypt_text(contents)
        with open(encrypt_path, 'w') as myfile:
            json.dump(res, myfile)

    def decrypt_file(self, pathfile):

        base_dir = os.path.dirname(os.path.abspath(__file__))

        encrypt_path = os.path.join(base_dir, pathfile)
        decrypt_path = os.path.join(base_dir, 'message_decrypted.txt')

        with open(encrypt_path, 'r') as myfile:
            contents = json.load(myfile)
        res = self.decrypt_text(contents)
        with open(decrypt_path, 'w') as myfile:
            myfile.write(res)


if __name__ == '__main__':
    p = pow(2, 607) - 1
    q = pow(2, 521) - 1

    print('Size of p:', len(str(p)))
    print('Size of q:', len(str(q)))

    rsa = RSA(p, q)
    rsa.public_key()
    rsa.private_key()

    sentence = 'codeforces'
    print('Initial message:', sentence)

    res = rsa.encrypt_text(sentence)
    print('Encrypted message :', res)

    res_inv = rsa.decrypt_text(res)
    print('Decrypted message :', res_inv)

    print('Success:', sentence == res_inv)

    rsa.encrypt_file('message_clean.txt')
    rsa.decrypt_file('message_encrypted.txt')
