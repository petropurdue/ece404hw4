# Homework Number: 04
# Name: Ziro Petro
# ECN Login: petrop
# Due Date: January 28 2020
# Python Interpreter: Python 3.5

import sys
from BitVector import *

AES_modulus = BitVector(bitstring='100011011') #MAKE SURE THIS IS WHATI THINK IT IS

def gen_key_schedule_128(key_bv):
    byte_sub_table = gen_subbytes_table()
    #  We need 44 keywords in the key schedule for 128 bit AES.  Each keyword is 32-bits
    #  wide. The 128-bit AES uses the first four keywords to xor the input block with.
    #  Subsequently, each of the 10 rounds uses 4 keywords from the key schedule. We will
    #  store all 44 keywords in the following list:
    key_words = [None for i in range(44)]
    round_constant = BitVector(intVal=0x01, size=8)
    for i in range(4):
        key_words[i] = key_bv[i * 32: i * 32 + 32]
    for i in range(4, 44):
        if i % 4 == 0:
            kwd, round_constant = gee(key_words[i - 1], round_constant, byte_sub_table)
            key_words[i] = key_words[i - 4] ^ kwd
        else:
            key_words[i] = key_words[i - 4] ^ key_words[i - 1]
    return key_words


def gen_key_schedule_192(key_bv):
    byte_sub_table = gen_subbytes_table()
    #  We need 52 keywords (each keyword consists of 32 bits) in the key schedule for
    #  192 bit AES.  The 192-bit AES uses the first four keywords to xor the input
    #  block with.  Subsequently, each of the 12 rounds uses 4 keywords from the key
    #  schedule. We will store all 52 keywords in the following list:
    key_words = [None for i in range(52)]
    round_constant = BitVector(intVal=0x01, size=8)
    for i in range(6):
        key_words[i] = key_bv[i * 32: i * 32 + 32]
    for i in range(6, 52):
        if i % 6 == 0:
            kwd, round_constant = gee(key_words[i - 1], round_constant, byte_sub_table)
            key_words[i] = key_words[i - 6] ^ kwd
        else:
            key_words[i] = key_words[i - 6] ^ key_words[i - 1]
    return key_words

def gen_key_schedule_256(key_bv):
    byte_sub_table = gen_subbytes_table()
    #  We need 60 keywords (each keyword consists of 32 bits) in the key schedule for
    #  256 bit AES. The 256-bit AES uses the first four keywords to xor the input
    #  block with.  Subsequently, each of the 14 rounds uses 4 keywords from the key
    #  schedule. We will store all 60 keywords in the following list:
    key_words = [None for i in range(60)]
    round_constant = BitVector(intVal=0x01, size=8)
    for i in range(8):
        key_words[i] = key_bv[i * 32: i * 32 + 32]
    for i in range(8, 60):
        if i % 8 == 0:
            kwd, round_constant = gee(key_words[i - 1], round_constant, byte_sub_table)
            key_words[i] = key_words[i - 8] ^ kwd
        elif (i - (i // 8) * 8) < 4:
            key_words[i] = key_words[i - 8] ^ key_words[i - 1]
        elif (i - (i // 8) * 8) == 4:
            key_words[i] = BitVector(size=0)
            for j in range(4):
                key_words[i] += BitVector(intVal=
                                          byte_sub_table[key_words[i - 1][8 * j:8 * j + 8].intValue()], size=8)
            key_words[i] ^= key_words[i - 8]
        elif ((i - (i // 8) * 8) > 4) and ((i - (i // 8) * 8) < 8):
            key_words[i] = key_words[i - 8] ^ key_words[i - 1]
        else:
            sys.exit("error in key scheduling algo for i = %d" % i)
    return key_words

def get_key_from_user(keydoc):
    fptr = open(keydoc)
    key = fptr.readline()
    print(key)
    keysize = len(key) * 8
    print(keysize)


    if sys.version_info[0] == 3:
        #keysize = int(input("\nAES Key size:  "))                  removed as it is calculated in previous lines
        assert any(x == keysize for x in [128, 192, 256]), \
            "keysize is wrong (must be one of 128, 192, or 256) --- aborting"
        #key = input("\nEnter key (any number of chars):  ")
    else:
        #keysize = int(raw_input("\nAES Key size:  "))
        assert any(x == keysize for x in [128, 192, 256]), \
            "keysize is wrong (must be one of 128, 192, or 256) --- aborting"
        #key = raw_input("\nEnter key (any number of chars):  ")
    key = key.strip()
    key += '0' * (keysize // 8 - len(key)) if len(key) < keysize // 8 else key[:keysize // 8]
    key_bv = BitVector(textstring=key)
    return keysize, key_bv

def gee(keyword, round_constant, byte_sub_table):
    '''
    This is the g() function you see in Figure 4 of Lecture 8.
    '''
    rotated_word = keyword.deep_copy()
    rotated_word << 8
    newword = BitVector(size = 0)
    for i in range(4):
        newword += BitVector(intVal = byte_sub_table[rotated_word[8*i:8*i+8].intValue()], size = 8)
    newword[:8] ^= round_constant
    round_constant = round_constant.gf_multiply_modular(BitVector(intVal = 0x02), AES_modulus, 8)
    return newword, round_constant

def gen_subbytes_table():
    subBytesTable = []
    c = BitVector(bitstring='01100011')
    for i in range(0, 256):
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
    return subBytesTable

def genTables():
    c = BitVector(bitstring='01100011')
    d = BitVector(bitstring='00000101')
    for i in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        # For bit scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For bit scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSubBytesTable.append(int(b))

def genkeyschedule(keysize):
    key_words = []
    print("Generating key schedule for keysize=", keysize, "...")
    if keysize == 128:
        key_words = gen_key_schedule_128(key_bv)
    elif keysize == 192:
        key_words = gen_key_schedule_192(key_bv)
    elif keysize == 256:
        key_words = gen_key_schedule_256(key_bv)
    else:
        sys.exit("wrong keysize --- aborting")
    print("Generated key schedule!")

    key_schedule = []
    print("\nEach 32-bit word of the key schedule is shown as a sequence of 4 one-byte integers:")
    for word_index, word in enumerate(key_words):
        keyword_in_ints = []
        for i in range(4):
            keyword_in_ints.append(word[i * 8:i * 8 + 8].intValue())
        if word_index % 4 == 0: print("\n")
        print("aword %d:  %s" % (word_index, str(keyword_in_ints)))
        key_schedule.append(keyword_in_ints)
    num_rounds = None
    if keysize == 128: num_rounds = 10
    if keysize == 192: num_rounds = 12
    if keysize == 256: num_rounds = 14
    round_keys = [None for i in range(num_rounds + 1)]
    for i in range(num_rounds + 1):
        round_keys[i] = (key_words[i * 4] + key_words[i * 4 + 1] + key_words[i * 4 + 2] +
                         key_words[i * 4 + 3]).get_bitvector_in_hex()
    print("\n\nRound keys in hex (first key for input block):\n")
    for round_key in round_keys:
        print(round_key)

def sreplace(subBytesTable,row,column):
    return subBytesTable[row.int_val()*16+column.int_val()]

def rowshift(inputarr):
    #convert the 4 columns into 4 rows
    start = []
    for k in range(4):
        rowarr = []
        for j in range(4):
            temparr = inputarr[j]
            rowarr.append(temparr[k])
        start.append(rowarr)
    #print(start)

    #do nothing to row one
    temp1 = start[0]

    #shift row 2 left 1
    temp2 = []
    interestrow = start[1]
    for i in range(1,4):
        temp2.append(interestrow[i])
    temp2.append(interestrow[0])

    #shift row 2 right two
    temp3 = []
    interestrow = start[2]
    for i in range(2):
        temp3.append(interestrow[i+2])
    for i in range(2):
        temp3.append(interestrow[i])

    # shift row 3 right one
    temp4 = []
    interestrow = start[3]
    temp4.append(interestrow[3])
    for i in range(3):
        temp4.append(interestrow[i])

    #append the newly made rows
    returnarray = [temp1,temp2,temp3,temp4]
    return returnarray


def colshift(inputarr):
    multarr = [2,3,1,1,1,2,3,1,1,1,2,3,3,1,1,2]
    #print(len(inputarr))
    #print("columnshift received",inputarr)
    retarr = []
    for i in range(16):
        # print(multarr[4*row+col],inputarr[4*row+col],"^") #OLD and EFFICIENT solution (INCOMPLETE because I am LAZY)
        row = i//4
        col = i % 4
        if (i<4): #if in first row
            retarr.append((multarr[i] * inputarr[i+4]) ^ (multarr[i]*inputarr[i+4]) ^ inputarr[i+8] ^ inputarr[i+12])
        if ((4<i) & (i < 8)):
            retarr.append(inputarr[i-4] ^ (2*inputarr[i]) ^ (3 * inputarr[i+4]) ^ inputarr[i+8])
        if ((8 < i) & (i < 12)):
            retarr.append((inputarr[i - 8]) ^ inputarr[i - 4] ^ (2 * inputarr[i]) ^ (3 * inputarr[i + 4]))
        if ((12 < i) & (i < 16)):
            retarr.append((3*inputarr[i - 12]) ^ inputarr[i - 8] ^ (inputarr[i-4]) ^ (2 * inputarr[i]))
    return retarr #i named return arr retarr, oh what a timesaver I am

def decompress(beginarray):
    temp = []
    for i in beginarray:
        for j in i:
            if (isinstance(j,list)):
                for k in j:
                    temp.append(k)
            else:
                temp.append(j)
    return temp

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    readsize = 128
    bitsize = 8

    print(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

    #Get key from keyfile
    print("Getting key...")
    keysize, key_bv = get_key_from_user(sys.argv[3])
    print("Got key!")

    #Generate key schedule + S table
    #genkeyschedule(keysize)
    AES_modulus = BitVector(bitstring='100011011')
    subBytesTable = []  # for encryption
    invSubBytesTable = []  # for decryption
    genTables()

    #Get file data
    mptr = open(sys.argv[2])
    mtxt = mptr.readline()
    mbv = BitVector(textstring=mtxt)
    mbv.pad_from_right(len(mbv)%8)

    #Single byte based Substitution
    SBBS = []
    print(mbv)
    print(len(mbv))
    for i in range(0,len(mbv),8):
        SBBS.append(sreplace(subBytesTable,mbv[i:i+4],mbv[i+4:i+8]))
    print("SBBS:",SBBS)

    #rowwise permutation
    county = 1
    temparr = []
    RSarr = []
    sixteens = 0
    coolarr = []
    for i in range(1,len(SBBS)+1):
        if (county == 16):
            itno = sixteens * 16
            for j in range(4):
                #print(4*j+itno,4*j+itno+4)
                #print(itno,j)
                groovyarr = SBBS[(4*j+itno):(4*j+itno+4)]
                coolarr.append(groovyarr)
            county=0 #make sure its 0 because its about to go up to 1 in the next line
            sixteens+=1
            RSarr.append(rowshift(coolarr))
        county+=1
    RSarr = decompress(RSarr)
    print("RS  :",RSarr)

    #columnwise mixing
    CSarr = []
    print(len(RSarr))
    for i in range(0,len(RSarr),16):
        sendarr = RSarr[(i):(i+16)]
        if (len(sendarr) == 16):
            temparr = colshift(sendarr)
            CSarr.append(temparr)
        else:
            print("nice try, bucko. Unfortunately for you,",sendarr,"just ain't cuttin' the bill!")
            temparr = []
        sixteens+=1
    decompress(CSarr)
    print("CSARR:",CSarr)

    # single byte based substitution
    # rowwise permutation
    # columnwise mixing
    # addition of round key

