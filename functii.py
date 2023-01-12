import cv2
import numpy as np

def nextButon(top, img, matri, matriCopy):

    print("Next")
    top.quit()
    cv2.destroyAllWindows()

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver



def HoughLines(img, imgContour):
    lines = cv2.HoughLinesP(img, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(imgContour, (x1, y1), (x2, y2), (0, 255, 0), 2)
        print(line)


def afisareMatrice(matri):

    imgStackTest = stackImages(0.6, (
    [matri[0][0], matri[0][1], matri[0][2], matri[0][3], matri[0][4], matri[0][5], matri[0][6], matri[0][7]]
    , [matri[1][0], matri[1][1], matri[1][2], matri[1][3], matri[1][4], matri[1][5], matri[1][6], matri[1][7]]
    , [matri[6][0], matri[6][1], matri[6][2], matri[6][3], matri[6][4], matri[6][5], matri[6][6], matri[6][7]]
    , [matri[7][0], matri[7][1], matri[7][2], matri[7][3], matri[7][4], matri[7][5], matri[7][6], matri[7][7]]))
    cv2.imshow("Matrice", imgStackTest)

def afisareMatriceCopy(matri):

    imgStackTest = stackImages(0.6, (
    [matri[0][0], matri[0][1], matri[0][2], matri[0][3], matri[0][4], matri[0][5], matri[0][6], matri[0][7]]
    , [matri[1][0], matri[1][1], matri[1][2], matri[1][3], matri[1][4], matri[1][5], matri[1][6], matri[1][7]]
    , [matri[6][0], matri[6][1], matri[6][2], matri[6][3], matri[6][4], matri[6][5], matri[6][6], matri[6][7]]
    , [matri[7][0], matri[7][1], matri[7][2], matri[7][3], matri[7][4], matri[7][5], matri[7][6], matri[7][7]]))
    cv2.imshow("C", imgStackTest)


def matricePatrate(img, matri):
    a = 0
    b = 0
    for i in range(0, img.shape[0], 45):
        for j in range(0, img.shape[1], 45):
            cv2.rectangle(img, (i, j), (i+40, j+40), (0, 255, 0), 2)
            imgCropped = img[j:j+40, i:i+40]
            matri[a][b] = imgCropped
            if a < 8:
                a += 1
            else:
                a = 0
                b += 1
            cv2.imshow("Matrice", img)
            cv2.waitKey(1)
    afisareMatrice(matri)

def mseCalc(matri, matriCopy, i, j):
    mse=((matri[i][j] - matriCopy[i][j]) ** 2).mean()
    print("MSE:", mse)
    return mse
def cautareSchimbare(matri, matriCopy, sah, player, img):
    if player == 1:
        for i in range(0, 8):
            for j in range(0, 8):
                #mean squared error
                if mseCalc(matri,matriCopy, i, j) > 45:
                    print("Schimbare")
                    print(i, j)
                    #PION ALB
                    if(sah[i][j] == "P"):
                        print("Pion mutat")
                        sah[i][j] = " "
                        #verificam pozitia pionului
                        #un pas in fata
                        if(mseCalc(matri,matriCopy, i+1, j) > 45):
                            sah[i+1][j] = "P"
                        else:
                            #2 pasi in fata
                            if (mseCalc(matri,matriCopy, i+2, j) > 45) and i == 1:
                                sah[i+2][j] = "P"
                            else:
                                #diagonala dreapta
                                if(mseCalc(matri,matriCopy, i+1, j+1) > 45) and sah[i+1][j+1] != " ":
                                    sah[i+1][j+1] = "P"
                                    print("Pion capturat")
                                else:
                                    #diagonala stanga
                                    if(mseCalc(matri,matriCopy, i+1, j-1) > 45) and sah[i+1][j-1] != " ":
                                        sah[i+1][j-1] = "P"
                                        print("Pion capturat")
                                    else:
                                        print("Mutare invalida")
                    else:
                        if(sah[i][j] == "T"):
                            print("turn mutat")
                            sah[i][j] = " "
                            #verificam pozitia turnului
                            for i1 in range(0,8):
                                if(mseCalc(matri,matriCopy, i1, j) > 45):
                                    sah[i1][j] = "T"
                                    break
                                else:
                                    if(mseCalc(matri,matriCopy, i, i1) > 45):
                                        sah[i][i1] = "T"
                                        break
                                    else:
                                        print("Mutare invalida")
                        else:
                            if(sah[i][j] ==  "C"):
                                print("cal mutat")
                                sah[i][j] = " "
                                #verificam pozitia calului
                                for i1 in range(0,8):
                                    for j1 in range(0,8):
                                        if(np.array_equal(matriCopy[i1][j1], matri[i1][j1]) == False):
                                            if(abs(i1-i) == 2 and abs(j1-j) == 1):
                                                sah[i1][j1] = "C"
                                                break
                                            else:
                                                if(abs(i1-i) == 1 and abs(j1-j) == 2):
                                                    sah[i1][j1] = "C"
                                                    break
                                                else:
                                                    print("Mutare invalida")
                            else:
                                if(sah[i][j] == "N"):
                                    print("nebun mutat")
                                    sah[i][j] = " "
                                    #verificam pozitia nebunului
                                    for i1 in range(0,8):
                                        for j1 in range(0,8):
                                            if(mseCalc(matri,matriCopy, i1, j1) > 45):
                                                if(abs(i1-i) == abs(j1-j)):
                                                    sah[i1][j1] = "N"
                                                    break
                                                else:
                                                    print("Mutare invalida")
                                else:
                                    if(sah[i][j] == "R"):
                                        print("regina mutat")
                                        sah[i][j] = " "
                                        #verificam pozitia reginei
                                        for i1 in range(0,8):
                                            for j1 in range(0,8):
                                                if(np.array_equal(matriCopy[i1][j1], matri[i1][j1]) == False):
                                                    if(abs(i1-i) == abs(j1-j)):
                                                        sah[i1][j1] = "R"
                                                        break
                                                    else:
                                                        if(abs(i1-i) == 0 or abs(j1-j) == 0):
                                                            sah[i1][j1] = "R"
                                                            break
                                                        else:
                                                            print("Mutare invalida")
                                    else:
                                        if(sah[i][j] == "K"):
                                            print("reg mutat")
                                            sah[i][j] = " "
                                            #verificam pozitia regelui
                                            for i1 in range(0,8):
                                                for j1 in range(0,8):
                                                    if(np.array_equal(matriCopy[i1][j1], matri[i1][j1]) == False):
                                                        if(abs(i1-i) <= 1 and abs(j1-j) <= 1):
                                                            sah[i1][j1] = "K"
                                                            break
                                                        else:
                                                            print("Mutare invalida")


                    player = 2
                    print("Umreaza player 2")
                    matricePatrate(img, matriCopy)
                    return player
    else:
        for i in range(7, 0, -1):
            for j in range(7, 0, -1):
                if mseCalc(matri,matriCopy, i, j) > 45:

                    #PION NEGRU
                    if (sah[i][j] == "P"):
                        print("Pion mutat")
                        sah[i][j] = " "
                        # verificam pozitia pionului
                        #un pas in fata
                        if (mseCalc(matri,matriCopy, i-1, j) > 45):
                            sah[i - 1][j] = "P"
                        else:
                            # 2 pasi in fata
                            if (mseCalc(matri,matriCopy, i-2, j) > 45) and i == 6:
                                sah[i - 2][j] = "P"
                            else:
                                # diagonala stanga
                                if (mseCalc(matri,matriCopy, i-1, j-1) > 45) and sah[i - 1][j - 1] != " ":
                                    sah[i - 1][j - 1] = "P"
                                    print("Pion capturat")
                                else:
                                    #diagonala dreapta
                                    if (mseCalc(matri,matriCopy, i-1, j+1) > 45) and sah[i - 1][j + 1] != " ":
                                        sah[i - 1][j + 1] = "P"
                                        print("Pion capturat")
                                    else:
                                        print("Mutare invalida")
                    else:
                        if(sah[i][j] == "T"):
                            print("turn mutat")
                            sah[i][j] = " "
                            #verificam pozitia turnului
                            for i1 in range(6, 0, -1):
                                print("Ajunge aici")
                                if(mseCalc(matri,matriCopy, i1, j) > 45):
                                    sah[i1-1][j] = "T"
                                    break
                                else:
                                    if(mseCalc(matri,matriCopy, i, i1) > 45):
                                        sah[i][i1] = "T"
                                        break
                                    #else:
                                        #print("Mutare invalida")
                        else:
                            if(sah[i][j] ==  "C"):
                                print("cal mutat")
                                sah[i][j] = " "
                                #verificam pozitia calului
                                for i1 in range(7, 0, -1):
                                    for j1 in range(7, 0, -1):
                                        if(np.array_equal(matriCopy[i1][j1], matri[i1][j1]) == False):
                                            if(abs(i1-i) == 2 and abs(j1-j) == 1):
                                                sah[i1][j1] = "C"
                                                break
                                            else:
                                                if(abs(i1-i) == 1 and abs(j1-j) == 2):
                                                    sah[i1][j1] = "C"
                                                    break
                                                else:
                                                    print("Mutare invalida")
                            else:
                                if(sah[i][j] == "N"):
                                    print("nebun mutat")
                                    sah[i][j] = " "
                                    #verificam pozitia nebunului
                                    for i1 in range(7, 0, -1):
                                        for j1 in range(7, 0, -1):
                                            if(np.array_equal(matriCopy[i1][j1], matri[i1][j1]) == False):
                                                if(abs(i1-i) == abs(j1-j)):
                                                    sah[i1][j1] = "N"
                                                    break
                                                else:
                                                    print("Mutare invalida")
                                else:
                                    if(sah[i][j] == "R"):
                                        print("regina mutat")
                                        sah[i][j] = " "
                                        #verificam pozitia reginei
                                        for i1 in range(7, 0, -1):
                                            for j1 in range(7, 0, -1):
                                                if(np.array_equal(matriCopy[i1][j1], matri[i1][j1]) == False):
                                                    if(abs(i1-i) == abs(j1-j)):
                                                        sah[i1][j1] = "R"
                                                        break
                                                    else:
                                                        if(abs(i1-i) == 0 or abs(j1-j) == 0):
                                                            sah[i1][j1] = "R"
                                                            break
                                                        else:
                                                            print("Mutare invalida")
                                    else:
                                        if(sah[i][j] == "K"):
                                            print("reg mutat")
                                            sah[i][j] = " "
                                            #verificam pozitia regelui
                                            for i1 in range(7, 0, -1):
                                                for j1 in range(7, 0, -1):
                                                    if(np.array_equal(matriCopy[i1][j1], matri[i1][j1]) == False):
                                                        if(abs(i1-i) <= 1 and abs(j1-j) <= 1):
                                                            sah[i1][j1] = "K"
                                                            break
                                                        else:
                                                            print("Mutare invalida")

                    player = 1;
                    print("Umreaza player 1")
                    matricePatrate(img, matriCopy)
                    return player
    print("Nu este nici o schimbare")
    return False

