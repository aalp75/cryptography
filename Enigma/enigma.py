import os

class Enigma:
    def __init__(self):
        # Rotors
        ri = [4, 10, 12, 5, 11, 6, 3, 16, 21, 25, 13, 19, 14, 22, 24, 7, 23, 20, 18, 15, 0, 8, 1, 17, 2, 9]  # EKMFLGDQVZNTOWYHXUSPAIBRCJ
        rii = [0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 7, 22, 19, 12, 2, 16, 6, 25, 13, 15, 24, 5, 21, 14, 4]  # AJDKSIRUXBLHWTMCQGZNPYFVOE
        riii = [1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21, 25, 13, 24, 4, 8, 22, 6, 0, 10, 12, 20, 18, 16, 14]  # BDFHJLCPRTXVZNYEIWGAKMUSQO
        riv = [4, 18, 14, 21, 15, 25, 9, 0, 24, 16, 20, 8, 17, 7, 23, 11, 13, 5, 19, 6, 10, 3, 2, 12, 22, 1]  # ESOVPZJAYQUIRHXLNFTGKDCMWB
        rv = [21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13, 7, 11, 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10]  # VZBRGITYUPSDNHLXAWMJQOFECK

        self.rotors = [ri, rii, riii, riv, rv]

        self.changements_rotors = [17, 5, 22, 10, 0]

        # Reflectors
        ref_b = [24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19]  # YRUHQSLDPXNGOKMIEBFZCWVJAT
        ref_c = [17, 3, 14, 1, 9, 13, 19, 10, 21, 4, 7, 12, 11, 5, 2, 22, 25, 0, 23, 6, 24, 8, 15, 18, 20, 16]  # DOBJNTKVEHMLFCWZAXGYIPSUQ

        self.ref = [ref_b, ref_c]

        # Plugboard of 10 connexion
        self.plugboard_map = [i for i in range(26)]

        # Initial Setup
        self.rotor_setup = [0, 1, 2]  # Rotor Arrangements
        self.reflect_setup = 0  # 0 for RefB and 1 for RefC
        self.rotor_init_pos = [0, 0, 0]

        # Evolution of rotors
        self.rotor_current_pos = [0, 0, 0]

    def set_rotors(self):  # Force Deep copy
        for i in range(3):
            self.rotor_current_pos[i] = self.rotor_init_pos[0]

    def reflector(self, ind):
        return self.ref[self.reflect_setup][ind]

    def plugboard(self, ind):
        return self.plugboard_map[ind]

    def rotor(self, number_rotor, order, ind):
        return self.rotors[number_rotor][(ind + self.rotor_current_pos[order]) % 26]

    def rotor_inv(self, number_rotor, order, ind):
        res = 0
        for i in range(26):
            if ind == self.rotors[number_rotor][(i + self.rotor_current_pos[order]) % 26]:
                res = i
        return res

    def show(self):
        print('\033[1m' + 'Enigma Settings' + '\033[0m')
        print("Plugboard :", self.plugboard_map)
        tmp = [0, 0, 0]
        for i in range(3):
            tmp[i] = self.rotor_setup[i] + 1
        print("Rotor Setup : ", tmp)
        print("ReflectSetut :", self.reflect_setup)
        print("RotorInitPos :", self.rotor_init_pos)

    def reset(self):
        self.plugboard_map = [i for i in range(26)]

    def setup(
        self,
        new_plugboard,
        new_rotor_init_pos=['A', 'A', 'A'],
        new_rotor_setup=[1, 2, 3],
        new_reflect_setup=0,
    ):
        self.reset()
        for co in new_plugboard:
            self.plugboard_map[ord(co[0]) - 65] = ord(co[1]) - 65
            self.plugboard_map[ord(co[1]) - 65] = ord(co[0]) - 65

        for i in range(3):
            self.rotor_init_pos[i] = ord(new_rotor_init_pos[i]) - 65

        for i in range(3):
            self.rotor_setup[i] = new_rotor_setup[i] - 1

        self.reflect_setup = new_reflect_setup

    def encrypt_one(self, ind):  # encrypt from a number in 0,...,25
        tmp = ind
        tmp = self.plugboard(ind)

        for i in range(3):
            tmp = self.rotor(self.rotor_setup[i], i, tmp)

        tmp = self.reflector(tmp)

        for i in range(3):
            tmp = self.rotor_inv(self.rotor_setup[2 - i], 2 - i, tmp)

        tmp = self.plugboard(tmp)
        return tmp

    def encrypt_list(self, list_ind):  # encrypt from a list of number in 0,...,25
        res = []

        for ind in list_ind:
            res.append(self.encrypt_one(ind))

            self.rotor_current_pos[0] = (self.rotor_current_pos[0] + 1) % 26

            if self.rotor_current_pos[0] == self.changements_rotors[self.rotor_setup[0]]:
                self.rotor_current_pos[1] = (self.rotor_current_pos[1] + 1) % 26

            if self.rotor_current_pos[1] == self.changements_rotors[self.rotor_setup[1]]:
                self.rotor_current_pos[2] = (self.rotor_current_pos[2] + 1) % 26

        return res

    def encrypt_word(self, word):  # crypte 1 word write in Uppercase
        list_ind = []
        for char in word:
            list_ind.append(ord(char) - 65)

        tmp = self.encrypt_list(list_ind)

        res = ''
        for ind in tmp:
            res = res + chr(ind + 65)

        return res

    def encrypt_sentence(self, sentence):
        self.set_rotors()
        res = ""

        for word in sentence.split():
            res = res + " " + self.encrypt_word(word)

        return res[1:]

    def encrypt_file(self, pathfile_clean, pathfile_encrypt):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        clean_path = os.path.join(base_dir, pathfile_clean)
        encrypt_path = os.path.join(base_dir, pathfile_encrypt)

        with open(clean_path, 'r') as myfile:
            sentence = self.encrypt_sentence(myfile.read())

        with open(encrypt_path, 'w') as myfile:
            myfile.write(sentence)

if __name__ == '__main__':
    enigma = Enigma()
    enigma.show()

    # setup the machine

    plug = ['LH','GO','MA','BZ']
    rotsetup = [5, 4, 2]
    rotorpos = ['M', 'R', 'Z']

    refsetup = 1
    enigma.setup(plug, rotorpos, rotsetup, refsetup)
    enigma.show()

    sentence = 'I WILL BE LATE PLEASE FORGIVE ME'
    print(sentence)
    res = enigma.encrypt_sentence(sentence)
    print(res)
    res_inv = enigma.encrypt_sentence(res)
    print(res_inv)
    print("Succes :",sentence==res_inv)

    sentence = 'I REALLY MISS THE TIME I USED TO SWIM EVERYDAY'
    print(sentence)
    res = enigma.encrypt_sentence(sentence)
    print(res)
    res_inv = enigma.encrypt_sentence(res)
    print(res_inv)
    print("Succes :",sentence==res_inv)

    sentence = 'HELLO MY NAME IS ANTOINE AND I AM SENDING YOU A MESSSAGE THANKS TO ENIGMA MACHINE'
    print(sentence)
    res = enigma.encrypt_sentence(sentence)
    print(res)
    res_inv = enigma.encrypt_sentence(res)
    print(res_inv)
    print("Succes :",sentence==res_inv)

    enigma.encrypt_file('message_clean.txt','message_encrypted.txt')
    enigma.encrypt_file('message_encrypted.txt','message_decrypted.txt')