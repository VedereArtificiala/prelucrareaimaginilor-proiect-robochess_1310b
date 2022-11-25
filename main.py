import cv2
import numpy as np
from tkinter import *
from functii import *

def main():
    widthImg, heightImg = 500, 500
    ok=0
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    #Citit imagine
    img = cv2.imread("Images/TablaSah/imagine1.png")
    contorImagine = 1

    #Creare matrice de imagini
    matri = np.zeros((8, 8), dtype=object)
    matriCopy = np.zeros((8, 8), dtype=object)
    matricePatrate(img, matriCopy)

    #Creare matrice de sah virtuala
    sah = np.array([["T", "C", "N", "R", "D", "N", "C", "T"],
                    ["P", "P", "P", "P", "P", "P", "P", "P"],
                    [" ", " ", " ", " ", " ", " ", " ", " "],
                    [" ", " ", " ", " ", " ", " ", " ", " "],
                    [" ", " ", " ", " ", " ", " ", " ", " "],
                    [" ", " ", " ", " ", " ", " ", " ", " "],
                    ["P", "P", "P", "P", "P", "P", "P", "P"],
                    ["T", "C", "N", "R", "D", "N", "C", "T"]])

    player = 1;


    imgBlank = np.zeros_like(img)

    while True:

        #Creare imagine contur
        imgContour = img.copy()


        #Prelucrare imagine
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
        imgCanny = cv2.Canny(imgGray, 300, 600)
        imgDilate = cv2.dilate(imgCanny, kernel, iterations=1)


        #Detectare linii + Introducere in matrice de patrate fiecare patrat din imagine
        HoughLines(imgDilate, imgContour)
        matricePatrate(img, matri)


        #Afisare imagini
        imgStack = stackImages(0.6,([img, imgBlank, imgContour],
                                [imgCanny, imgDilate, imgBlank]))

        cv2.imshow("Analiza", imgStack)

        # cv2.setMouseCallback('Stack', click_event)

        #Cauta daca o piesa a fost mutata
        if ok==1:
            cautareSchimbare(matri, matriCopy, sah, player, img)
            if(player==1):
                player=2
            else:
                player=1

        #Afisare Tabla Sah
        for i in range(0, 8):
            for j in range(0, 8):
                print(sah[i][j], end=" ")
            print()


        # buton
        top = Tk()
        B = Button(top, text="Next", command= lambda:nextButon(top, img, matri, matriCopy))
        B.pack()
        top.mainloop()

        #Schimbare imagine urmatoare
        if contorImagine==1:
            img = cv2.imread("Images/TablaSah/imagine2.png")
            contorImagine += 1
        else:
            if contorImagine==2:
                img = cv2.imread("Images/TablaSah/imagine3.png")
                contorImagine += 1
            else:
                img = cv2.imread("Images/TablaSah/imagine4.png")
        ok=1
        cv2.waitKey(0)
        top.destroy()






main()



