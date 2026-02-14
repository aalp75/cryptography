import copy
import random

import matplotlib.pyplot as plt
import numpy as np
import os


alphabet = list(range(26))

freq = [4, 0, 8, 18, 13, 17, 19, 14, 11, 20, 3, 2, 12, 15, 6, 1, 21, 7, 5, 16, 24, 23, 9, 10, 22, 25]  # EAI...


prob_matrix = np.zeros((27, 27))
file = open("mh/data.txt", "r")
n = 0
for line in file:
    n += 1
    letter = ord(line[0])
    if letter >= 97 and letter <= 122:
        letter = letter - 97
        prob_matrix[26, letter] += 1
    for i in range(len(line) - 1):
        letter = ord(line[i])
        if letter == 10:
            letter = 26
        if letter >= 97 and letter <= 122:
            letter = letter - 97
        next_letter = ord(line[i + 1])
        if next_letter == 10:
            next_letter = 26
        if next_letter >= 97 and next_letter <= 122:
            next_letter = next_letter - 97

        if letter <= 26 and next_letter <= 26:
            prob_matrix[letter, next_letter] += 1

prob_matrix = np.log(prob_matrix / n + 0.000001)
file.close()
print("There is", n, "words")

def compute_plausibility(tab):
    plausibility = 0
    n_plausibility = 0
    for i in range(len(tab) - 1):
        n_plausibility += 1
        plausibility += prob_matrix[tab[i], tab[i + 1]]
    return plausibility / n_plausibility


def permutation(tab):
    res = copy.deepcopy(tab)
    u1 = random.randint(0, 25)
    u2 = random.randint(0, 25)
    while u1 == u2:
        u2 = random.randint(0, 25)
    res[u1] = tab[u2]
    res[u2] = tab[u1]
    return res


def string_to_int(sentence, state=alphabet):
    res = []
    for i in range(len(sentence)):
        asc2 = ord(sentence[i])
        if asc2 == 32:
            res.append(26)
        else:
            res.append(state[asc2 - 97])
    return res


def int_to_string(sentence, state=alphabet):
    res = ""
    for i in range(len(sentence)):
        if sentence[i] == 26:
            res += " "
        else:
            res += chr(state[sentence[i]] + 97)
    return res


def crypt_sentence(res, key):
    for i in range(len(res)):
        if res[i] != 26:
            res[i] = key[res[i]]
    return res


def decrypt_sentence(res, key):
    for i in range(len(res)):
        if res[i] == 26:
            res[i] = " "
        else:
            for j in range(26):
                if key[j] == res[i]:
                    res[i] = chr(j + 97)
                    break
    return res

def decrypt_array(tab, key):
    res = []
    for i in range(len(tab)):
        if tab[i] == 26:
            res.append(26)
        else:
            for j in range(26):
                if key[j] == tab[i]:
                    res.append(j)
                    break
    return res

def compute_init_state(sentence):
    res = np.zeros(26)
    freq_here = np.zeros(26)
    for i in range(len(sentence)):
        letter = ord(sentence[i])
        if letter != 32:
            freq_here[letter - 97] += 1
    for i in range(26):
        index = np.where(freq_here == freq_here.max())[0][0]
        res[index] = int(freq[i])
        freq_here[index] = -1
    return res

def mh(sentence, t=1, max_iter=500000, min_iter=200, treshold=-1.5):
    print("This is my crypted sentence :")
    print(sentence)
    n_sentence = len(sentence)

    tab_crypt = string_to_int(sentence)
    x0 = compute_init_state(sentence)

    x0_try = decrypt_array(tab_crypt, x0)
    x0_plausibility = compute_plausibility(x0_try)

    best_score = x0_plausibility

    for i in range(max_iter):
        x_guess = permutation(x0)
        x_guess_try = decrypt_array(tab_crypt, x_guess)
        x_guess_plausibility = compute_plausibility(x_guess_try)

        r = np.exp((x_guess_plausibility - x0_plausibility) * n_sentence / t)

        if x_guess_plausibility > best_score:
            print("For %d iterations the plausibility is %0.2f" % (i, x_guess_plausibility))
            print(int_to_string(x_guess_try))
            best_score = x_guess_plausibility

        u = random.uniform(0, 1)
        if u < r:
            x0 = x_guess
            x0_try = x_guess_try
            x0_plausibility = x_guess_plausibility

    print("The key is :")
    for i in range(len(x0)):
        print(chr(int(alphabet[i] + 65)), ":", chr(int(x0[i] + 65)))
    print(int_to_string(x0_try))
    return int_to_string(x0_try)


if __name__ == "__main__":
    key = list(range(26))
    random.shuffle(key)

    test = "je suis le plus grand de ma classe et mon sac a dos est bleu"
    test_int = string_to_int(test)
    crypt_array = crypt_sentence(test_int, key)
    crypt_test = int_to_string(crypt_array)
    print(test)
    print(crypt_test)
    decrypt_test = decrypt_sentence(crypt_array, key)
    print(str(decrypt_test))
    mh(crypt_test)
