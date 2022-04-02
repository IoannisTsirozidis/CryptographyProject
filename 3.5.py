# I DO NOT own this code. This is a modified version of the professor's K.Draziotis' code
# found on the repository: https://github.com/drazioti/python_scripts/blob/master/numtheory/lfsr_project.py

# *****************************************************************************
#       Copyright (C) 2015 K.Draziotis <drazioti@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
# *****************************************************************************


from collections import deque


def bin_to_INT_list(string_bin):
    ilist = []
    for i in string_bin:
        if i == '1':
            ilist.append(1)
        else:
            ilist.append(0)

    return ilist


aDict = dict(zip('abcdefghijklmnopqrstuvwxyz.!?()-ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                 ['00000', '00001', '00010', '00011', '00100',
                  '00101', '00110', '00111', '01000',
                  '01001', '01010', '01011', '01100', '01101', '01110', '01111',
                  '10000', '10001', '10010', '10011',
                  '10100', '10101', '10110', '10111',
                  '11000', '11001',
                  '11010', '11011', '11100', '11101', '11110', '11111',
                  '00000', '00001', '00010', '00011', '00100',
                  '00101', '00110', '00111', '01000',
                  '01001', '01010', '01011', '01100', '01101', '01110', '01111',
                  '10000', '10001', '10010', '10011',
                  '10100', '10101', '10110', '10111',
                  '11000', '11001']))  # the function from our alphabet to 5-bit binary strings


# (Strings) Text to Binary   |   using aDict
# parameter: String in text form
# output: String in binary form
def text_enc(text):
    text = text[::-1]
    length = len(text)
    coded_text = ''
    for i in range(length):
        coded_text = aDict[text[i]] + coded_text
    return coded_text.lower()


# (Strings) Binary to Text   |   using aDict
# parameter: string in binary form
# output: string in lowercase, text form
def text_dec(binary_string):
    length = len(binary_string)
    inv_map = {v: k for k, v in aDict.items()}
    decoded_text = ''
    for i in range(0, length, 5):
        decoded_text = inv_map[binary_string[i:i + 5]] + decoded_text  # + in strings is the join function.
    decoded_text = decoded_text[::-1]
    return decoded_text.lower()


# parameter: A binary list (List of Integers 1 and 0)
# output: A single Integer, representing a sequenced XOR between the list's integers
def sumxor(l):
    r = 0
    for v in l:
        r = r ^ v
    return r


# parameters:
# param[0]- (String) Binary String (1s and 0s)
# param[1]- (String) Binary String (1s and 0s)

# output: (String) param[0] XOR param[1]
def string_xor(btext, key):
    cipher = []
    if len(btext) != len(key):
        print("key and message must have the same lengths!")
        return 0
    for i in range(len(btext)):
        cipher.append(int(btext[i]) ^ int(key[i]))  # xoring bit-bit
    cipher = ''.join(str(e) for e in cipher)
    return cipher


# parameters:
# seed: Binary List
# feedback: Binary List
# bits: Integer representing the len(text_enc('...')), the number of LFSR's repetitions and the key's length.
# flag: a flag.
# If flag==0 then it prints stuff.
# If flag==1, it does NOT print stuff

# outputs a Binary List (List of Integers 1 and 0)
def lfsr(seed,feedback,bits, flag):
    index_of_ones = []
    feedback_new = []
    for i in range(len(feedback)):
        if 1 in feedback:
            index_of_ones.append(feedback.index(1))
            feedback[feedback.index(1)] = 0
    feedback_new = index_of_ones    #this is a list which contains the positions of 1s in feedback list
    seed = deque(seed)              # make a new deque
    output = []
    if flag==0:
        print('initial seed :',seed)
    for i in range(bits):
        xor = sumxor([seed[j] for j in feedback_new])
        output.append(seed.pop()) #extract to output the right-most bit of current seed
        seed.appendleft(xor)      #insert from left the result of the previous xor
        if flag==0:
            print('state', i+1, 'of the lfsr :',seed)
    return output


# Converts a List to String...
def list_to_string(l):
    return ''.join(str(e) for e in l)


if __name__ == "__main__":

    # Create a list of lists, which contains every 10 digit binary number.
    # The Binary numbers produced are in form of a List Of Integers (1 and 0)
    listoflists = []
    n = 10
    for i in range(2 ** n):
        b = bin(i)[2:]
        l = len(b)
        b = str(0) * (n - l) + b
        listoflists.append(bin_to_INT_list(b))

    index_result = []
    key = [1, 0, 0, 1, 0, 1, 0, 0, 0, 1]
    feedback_polynomial = [0, 0, 0, 0, 0, 1, 1, 0, 1, 1]

    for i in range(len(listoflists)):
        feedback_polynomial1=feedback_polynomial.copy()
        #print(feedback_polynomial1)
        if lfsr(listoflists[i], feedback_polynomial1, 10, 1) == key:
            index_result.append(i)


    print(index_result)

    # The Above operation performs a Brute Force attack, to find the initial Seed:
    # knowing the feedback_polynomial,
    # the produced key,
    # and the number of repetitions which in this case are 10, same as the length of encrypted text in binary form.

    # The Integer index_result is the Index in listoflists which indicated the List[index_result],
    # that matched the brute force attack.
    seed1 = listoflists[811]
    print('seed: ',seed1)

    # ---------------------------------------------
    # In Exercise 3.5, the cipher_text given was:
    cipher_text = "i!))aiszwykqnfcyc!?secnncvch"

    # I'm going to convert this text-String into Binary-String, using the function: text_enc()
    bitstream = text_enc(cipher_text)

    feedback_polynomial1 = feedback_polynomial.copy()
    # Produce a new key with LFSR, using the seed, the feedback_polynomial, the length of bitstream, and 1
    new_key = lfsr(seed1, feedback_polynomial1, len(bitstream), 1)
    new_key1 = lfsr(listoflists[533], feedback_polynomial1, len(bitstream), 1)

    # Finally, perform bitstream XOR new_key and pass the result in the function =: text_dec()
    original_message = text_dec(string_xor(list_to_string(bitstream), list_to_string(new_key)))

    print('original: ',original_message)

#Brute Force Approach
"""
    for i in range(len(listoflists)):
        feedback_polynomial1=feedback_polynomial.copy()
        print(i, text_dec(string_xor(text_enc('i!))aiszwykqnfcyc!?secnncvch'),list_to_string(lfsr(listoflists[i], feedback_polynomial1, len(text_enc('i!))aiszwykqnfcyc!?secnncvch')), 1)))))
"""

"""
    text = 'Simplecanbeharderthancomplex'
    streambits = text_enc(text)
    initial_seed = [0, 0, 0, 0, 1, 0, 1, 0, 1, 1]
    O = lfsr(initial_seed, [0, 0, 0, 0, 0, 1, 1, 0, 1, 1], len(streambits), 1)
    keystream = list_to_string(O)
    print(text_dec(string_xor(text_enc(text),keystream)))
"""
