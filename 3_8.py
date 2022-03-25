import sys

abc = {
    'A': '00000', 'B': '00001', 'C': '00010', 'D': '00011', 'E': '00100', 'F': '00101', 'G': '00110', 'H': '00111',
    'I': '01000', 'J': '01001', 'K': '01010', 'L': '01011', 'M': '01100', 'N': '01101', 'O': '01110', 'P': '01111',
    'Q': '10000', 'R': '10001', 'S': '10010', 'T': '10011', 'U': '10100', 'V': '10101', 'W': '10110', 'X': '10111',
    'Y': '11000', 'Z': '11001', '.': '11010', '!': '11011', '?': '11100', '(': '11101', ')': '11110', '-': '11111'
}

help = """Run:
python 3_8.py -help for help message
python 3_8.py -e for encryption
python 3_8.py -d for decryption
"""

# returns the original text that is represented by the string of binary '1' and '0'
def bin_to_text(bin_text):
    encrypted = ''
    j = 1
    temp = ''

    for i in bin_text:
        if i == '1':
            temp += i
        else:
            temp += '0'

        if j % 5 == 0:
            encrypted += getkey(abc, temp)
            temp = ''
            j = 1
        else:
            j += 1

    return encrypted


# Additive function
def getkey(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            return key

    return "key doesn't exist"


# returns a string sequence based on the dictionary's keys that form the parameter text
def text_to_bin(text):
    s = ''
    for c in text:
        s += abc[c]
    return s


# returns an integer list based on string of '1' and '0'
def bin_to_INT_list(string_bin):
    ilist = []
    for i in string_bin:
        if i == '1':
            ilist.append(1)
        else:
            ilist.append(0)

    return ilist


# returns a String of 1s and 0s that are converted from integers from ilist
def intList_to_string_bit(ilist):
    s = ''
    for i in ilist:
        if i == 1:
            s += '1'
        else:
            s += '0'

    return s


# Key Scheduling Algorithm (KSA) returns a shuffled 256 bit array which was initially ordered.
# As an input there is a String input_key. The function translates the input_key to binary.
# Then based on the len(input_key) it performs swaps on the ordered array, shuffling it.
def KSA(input_key):
    key = bin_to_INT_list(text_to_bin(input_key))
    S = []
    for i in range(256):
        S.append(i)
    j = 0

    temp = 0
    for i in range(len(S)):
        j = (j + S[i] + key[i % len(key)]) % 256
        temp = S[i]
        S[i] = S[j]
        S[j] = temp

    return S

#The Pseudo-random generation algorithm (PRGA) constructs an array 'K', which has the same length
#as the plaintext in binary.The array K, is supposed to have pseudo-random elements (0-256) in each position
#based on the array S that was constructed with the Key Scheduling Algorithm (KSA).

def PRGA(S, plaintext):
    j = 0
    K = []
    s_temp = S

    pltx = bin_to_INT_list(text_to_bin(plaintext))

    for i in range(len(pltx)):
        i = (i + 1) % 256
        j = (j + s_temp[i]) % 256
        # swap s_temp[i] with s_temp[j]
        temp = s_temp[i]
        s_temp[i] = s_temp[j]
        s_temp[j] = temp

        K.append(s_temp[(s_temp[i] + s_temp[j]) % 256])

    return K


def Encrypt(plaintext, K):
    encrypted = []
    pltx = bin_to_INT_list(text_to_bin(plaintext))

    for i in range(len(pltx)):
        encrypted.append((K[i] ^ pltx[i]) % 2)

    return bin_to_text(intList_to_string_bit(encrypted))


def Decrypt(ciphertext, K):
    return Encrypt(ciphertext, K)


if __name__ == "__main__":
    #plaintext ='MISTAKESAREASSERIOUSASTHERESULTSTHEYCAUSE'
    #key_seed='HOUSE'
    #ciphertext='HVAIV(KX!VPR-FDTT?UIQ-RCYLISUCO?VBKNB?)KP'



    availableOpt = ['-d', '-e']
    if len(sys.argv) == 1 or sys.argv[1] not in availableOpt:
        print(help)
        exit(0)


    #decryption
    if sys.argv[1] == availableOpt[0]:
        plaintext = input("Encrypted message: ")
        key_seed = input("key_seed: ")
        print(Decrypt(plaintext, PRGA(KSA(key_seed), plaintext)))

    #encryption
    if sys.argv[1] == availableOpt[1]:
        plaintext = input("message: ")
        # message characters check
        k = 1
        while k == 1:
            for c in plaintext:
                if c not in abc.keys():
                    print('Invalid entry. Please use no white spacing and only the characters in abc dict.')
                    plaintext = input("message: ")

            k = 0

        key_seed = input("key_seed: ")
        # message characters check
        k = 1
        while k == 1:
            for c in plaintext:
                if c not in abc.keys():
                    print('Invalid entry. Please use no white spacing and only the characters in abc dict.')
                    plaintext = input("message: ")

            k = 0

        print(Encrypt(plaintext, PRGA(KSA(key_seed), plaintext)))
