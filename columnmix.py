from BitVector import *

def colshift(inputarr):
    multarr = [2,3,1,1,1,2,3,1,1,1,2,3,3,1,1,2]
    print(len(multarr))

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
            temp.append(j)
    print(temp)
    return temp

if __name__ == '__main__':
    print("test")
    beginarray = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
    #beginarray = [[1,5,9,13],[2,6,10,14],[3,7,11,15],[4,8,12,16]]
    print(beginarray)

    print("=================")
    salad = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,11,12,13,14,15,16,17,18,19,110,111,112,113,114,115,116]
    sixteensalad = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    endarray = colshift(sixteensalad)
    print(endarray)

    beginarray = decompress(beginarray)
    print(beginarray)
