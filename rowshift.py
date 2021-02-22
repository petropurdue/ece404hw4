def rowshift(inputarr):
    #convert the 4 columns into 4 rows
    start = []
    for k in range(4):
        rowarr = []
        for j in range(4):
            temparr = inputarr[j]
            rowarr.append(temparr[k])
        start.append(rowarr)
    print(start)

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

if __name__ == '__main__': #use this main to test the above function
    print("test")
    beginarray = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
    #beginarray = [[1,5,9,13],[2,6,10,14],[3,7,11,15],[4,8,12,16]]
    print(beginarray)
    endarray = rowshift(beginarray)
    print(endarray)

    print("=================")
    salad = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,11,12,13,14,15,16,17,18,19,110,111,112,113,114,115,116]
    county = 1
    sixteens = 0
    coolarr = []
    for i in range(1,len(salad)+1):
        if (county == 16):
            itno = sixteens * 16
            for j in range(4):
                #print(4*j+itno,4*j+itno+4)
                groovyarr = salad[4*j+itno:4*j+itno+4]
                coolarr.append(groovyarr)
            county=0 #make sure its 0 because its about to go up to 1 in the next line
            sixteens+=1
        county+=1
    print(coolarr)