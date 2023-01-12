import cv2
import numpy as np
from tkinter import *
from functii import *

def main():
    widthImg, heightImg = 500, 500
    ok=0
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))


    ok=1
    cap = cv2.VideoCapture(0)
    i=0
    while i<100:
        ret, frame = cap.read()
        i+=1

    height, width = frame.shape[:2]  # get the height and width of the frame
    # define the ROI
    x, y, w, h = (int(102), int(33), int(370), int(345))
    frame = cv2.getRectSubPix(frame, (w, h), (x + w//2 , y + h//2 ))
    contorImagine = 1

    #Creare matrice de imagini
    matri = np.zeros((9, 9), dtype=object)
    matriCopy = np.zeros((9, 9), dtype=object)
    matricePatrate(frame, matriCopy)

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
    ok1=0

    imgBlank = np.zeros_like(frame)

    while True:
        afisareMatriceCopy(matriCopy)
        if(ok==0):
            ret, frame = cap.read()
            if ret == True:
                cv2.imshow("Live Video", frame)  # display the frame
                height, width = frame.shape[:2]  # get the height and width of the frame
                # define the ROI
                x, y, w, h = (int(102), int(33), int(370), int(345))
                frame = cv2.getRectSubPix(frame, (w, h), (x + w // 2, y + h // 2))

        #Creare imagine contur
        imgContour = frame.copy()


        #Prelucrare imagine
        imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
        imgCanny = cv2.Canny(imgGray, 300, 600)
        imgDilate = cv2.dilate(imgCanny, kernel, iterations=1)


        #Detectare linii + Introducere in matrice de patrate fiecare patrat din imagine
        matricePatrate(frame, matri)


        #Afisare imagini
        imgStack = stackImages(0.6,([frame, imgBlank, imgContour],
                                [imgCanny, imgDilate, imgBlank]))

        cv2.imshow("Analiza", imgStack)


        #Cauta daca o piesa a fost mutata
        if ok==0:
            cautareSchimbare(matri, matriCopy, sah, player, frame)
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
        B = Button(top, text="Next", command= lambda:nextButon(top, frame, matri, matriCopy))
        B.pack()
        top.mainloop()

        ok=0
        cv2.waitKey(0)
        top.destroy()






main()



