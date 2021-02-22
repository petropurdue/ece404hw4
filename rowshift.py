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

if __name__ == '__main__':
    print("test")
    #beginarray = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
    beginarray = [[1,5,9,13],[2,6,10,14],[3,7,11,15],[4,8,12,16]]
    print(beginarray)
    endarray = rowshift(beginarray)
    print(endarray)