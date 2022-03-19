import random
import sys

abc = {
    'A': '00000', 'B': '00001', 'C': '00010', 'D': '00011', 'E': '00100', 'F': '00101', 'G': '00110', 'H': '00111',
    'I': '01000', 'J': '01001', 'K': '01010', 'L': '01011', 'M': '01100', 'N': '01101', 'O': '01110', 'P': '01111',
    'Q': '10000', 'R': '10001', 'S': '10010', 'T': '10011', 'U': '10100', 'V': '10101', 'W': '10110', 'X': '10111',
    'Y': '11000', 'Z': '11001', '.': '11010', '!': '11011', '?': '11100', '(': '11101', ')': '11110', '-': '11111'
}

help = """Run:
python 2_6.py -help for help message
python 2_6.py -e for encryption
python 2_6.py -d for decryption
"""

def encryption(message, key):
    bin_string = text_to_bin(message)
    bin_key = text_to_bin(key)

    # XOR operation between bits of bin_key and bin_message
    bin_encrypted = [(ord(a) ^ ord(b)) for a, b in zip(bin_key, bin_string)]

    return bin_to_text(bin_encrypted)


def decryption(ciphertext, key):
    bin_string = text_to_bin(ciphertext)
    bin_key = text_to_bin(key)

    bin_decrypted = [(ord(a) ^ ord(b)) for a, b in zip(bin_key, bin_string)]

    return bin_to_text(bin_decrypted)



def bin_to_text(bin_text):
    encrypted = ''
    j = 1
    temp = ''

    for i in bin_text:
        if i == 1:
            temp += '1'
        else:
            temp += '0'

        if j % 5 == 0:
            encrypted += getkey(abc, temp)
            temp = ''
            j = 1
        else:
            j += 1

    return encrypted

def text_to_bin(text):
    s = ''
    for c in text:
        s += abc[c]
    return s


def getkey(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            return key

    return "key doesn't exist"


if __name__ == "__main__":

    availableOpt = ['-d', '-e']
    if len(sys.argv) == 1 or sys.argv[1] not in availableOpt:
        print(help)
        exit(0)

    #encryption
    if sys.argv[1] == availableOpt[1]:
        msg = input("message: ")
        # message characters check
        k = 1
        while k == 1:
            for c in msg:
                if c not in abc.keys():
                    print('Invalid entry. For the message please use the characters in abc dict.')
                    msg = input("message: ")

            k = 0

        key=''
        for i in [random.choice(list(abc)) for i in range(len(msg))]:
            key+=i
        print('Random generated key: ',key)
        print('Encrypted message: ',encryption(msg, key))

    #decryption
    elif sys.argv[1] == availableOpt[0]:
        msg = input("Encrypted message: ")
        key = input("key: ")
        print(decryption(msg, key))
