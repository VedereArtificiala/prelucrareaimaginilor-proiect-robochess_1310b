import cv2
import numpy as np

# def click_event(event, x, y, flags, params):
#     # checking for left mouse clicks
#     if event == cv2.EVENT_LBUTTONDOWN:
#         # displaying the coordinates
#         # on the Shell
#         print(x, ' ', y)
#
#         # displaying the coordinates
#         # on the image window
#         font = cv2.FONT_HERSHEY_SIMPLEX
#         cv2.putText(img, str(x) + ',' +
#                     str(y), (x, y), font,
#                     1, (255, 0, 0), 2)
#         cv2.imshow('image', img)
#
#     # checking for right mouse clicks
#     if event == cv2.EVENT_RBUTTONDOWN:
#         # displaying the coordinates
#         # on the Shell
#         print(x, ' ', y)
#
#         # displaying the coordinates
#         # on the image window
#         font = cv2.FONT_HERSHEY_SIMPLEX
#         b = img[y, x, 0]
#         g = img[y, x, 1]
#         r = img[y, x, 2]
#         cv2.putText(img, str(b) + ',' +
#                     str(g) + ',' + str(r),
#                     (x, y), font, 1,
#                     (255, 255, 0), 2)
#         cv2.imshow('image', img)

# def getContours(img):
#     countours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#     for cnt in countours:
#         area = cv2.contourArea(cnt)
#         print(area)
#         cv2.drawContours(imgContour, cnt, -1, (255,0,0), 3)
#         peri = cv2.arcLength(cnt, True)
#         approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
#         print(len(approx))
#         objCor = len(approx)
#         x, y, w, h = cv2.boundingRect(approx)

# def crop(img):
#     r = cv2.selectROI("Select the area", img)
#     imgCrop = img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]]
#     return imgCrop

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
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
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
    # for i in range(0, 8):
    #     for j in range(0, 8):
    #         cv2.imshow("Matrice", matri[i][j])
    #         cv2.waitKey(0)
    imgStackTest = stackImages(0.6, (
    [matri[0][0], matri[0][1], matri[0][2], matri[0][3], matri[0][4], matri[0][5], matri[0][6], matri[0][7]]
    , [matri[1][0], matri[1][1], matri[1][2], matri[1][3], matri[1][4], matri[1][5], matri[1][6], matri[1][7]]
    , [matri[6][0], matri[6][1], matri[6][2], matri[6][3], matri[6][4], matri[6][5], matri[6][6], matri[6][7]]
    , [matri[7][0], matri[7][1], matri[7][2], matri[7][3], matri[7][4], matri[7][5], matri[7][6], matri[7][7]]))
    cv2.imshow("Matrice", imgStackTest)


def matricePatrate(img, matri):
    a = 0
    b = 0
    for i in range(0, img.shape[0], 65):
        for j in range(0, img.shape[1], 65):
            cv2.rectangle(img, (i, j), (i+50, j+50), (0, 255, 0), 2)
            imgCropped = img[j:j+50, i:i+50]
            matri[a][b] = imgCropped
            if a < 7:
                a += 1
            else:
                a = 0
                b += 1
            cv2.imshow("Matrice", img)
            cv2.waitKey(1)
    afisareMatrice(matri)

# def copyMatrice(img, matriCopy):
#     a = 0
#     b = 0
#     for i in range(0, img.shape[0], 65):
#         for j in range(0, img.shape[1], 65):
#             cv2.rectangle(img, (i, j), (i + 50, j + 50), (0, 255, 0), 2)
#             imgCropped = img[j:j + 50, i:i + 50]
#             matriCopy[a][b] = imgCropped
#             if a < 7:
#                 a += 1
#             else:
#                 a = 0
#                 b += 1
#     afisareMatrice(matriCopy)

def cautareSchimbare(matri, matriCopy, sah, player, img):
    if player == 1:
        for i in range(0, 8):
            for j in range(0, 8):
                if np.array_equal(matriCopy[i][j], matri[i][j]) == False:
                    print("Schimbare")
                    if(sah[i][j] == "P"):
                        print("Pion mutat")
                        sah[i][j] = " "
                        #verificam pozitia pionului
                        #un pas in fata
                        if(np.array_equal(matriCopy[i+1][j], matri[i+1][j]) == False):
                            sah[i+1][j] = "P"
                        else:
                            #2 pasi in fata
                            if (np.array_equal(matriCopy[i+2][j], matri[i+2][j]) == False) and i == 1:
                                sah[i+2][j] = "P"
                            else:
                                #diagonala dreapta
                                if(np.array_equal(matriCopy[i+1][j+1], matri[i+1][j+1]) == False) and sah[i+1][j+1] != " ":
                                    sah[i+1][j+1] = "P"
                                    print("Pion capturat")
                                else:
                                    #diagonala stanga
                                    if(np.array_equal(matriCopy[i+1][j-1], matri[i+1][j-1]) == False) and sah[i+1][j-1] != " ":
                                        sah[i+1][j-1] = "P"
                                        print("Pion capturat")
                                    else:
                                        print("Mutare invalida")
                    player = 2
                    print("Umreaza player 2")
                    matricePatrate(img, matriCopy)
                    return player
    else:
        for i in range(7, 0, -1):
            for j in range(7, 0, -1):
                if np.array_equal(matriCopy[i][j], matri[i][j]) == False:
                    if (sah[i][j] == "P"):
                        print("Pion mutat")
                        sah[i][j] = " "
                        # verificam pozitia pionului
                        #un pas in fata
                        if (np.array_equal(matriCopy[i - 1][j], matri[i - 1][j]) == False):
                            sah[i - 1][j] = "P"
                        else:
                            # 2 pasi in fata
                            if (np.array_equal(matriCopy[i - 2][j], matri[i - 2][j]) == False) and i == 6:
                                sah[i - 2][j] = "P"
                            else:
                                # diagonala stanga
                                if (np.array_equal(matriCopy[i - 1][j - 1], matri[i - 1][j - 1]) == False) and sah[i - 1][j - 1] != " ":
                                    sah[i - 1][j - 1] = "P"
                                    print("Pion capturat")
                                else:
                                    #diagonala dreapta
                                    if (np.array_equal(matriCopy[i - 1][j + 1], matri[i - 1][j + 1]) == False) and sah[i - 1][j + 1] != " ":
                                        sah[i - 1][j + 1] = "P"
                                        print("Pion capturat")
                                    else:
                                        print("Mutare invalida")
                    player = 1;
                    print("Umreaza player 1")
                    matricePatrate(img, matriCopy)
                    return player
    print("Nu este nici o schimbare")
    return False

