# Main.py

import cv2
import numpy as np
import os
import serial
import time
from time import gmtime, strftime

import sqlite3
import datetime

import DetectChars
import DetectPlates
import PossiblePlate


# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = True


###################################################################################################











def main():





    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()         # attempt KNN training

    if blnKNNTrainingSuccessful == False:                               # if KNN training was not successful
        print "\nerror: KNN traning was not successful\n"               # show error message
        return                                                          # and exit program
    # end if

    imgOriginalScene  = cv2.imread("test.jpg")               # open image  18/ 19/

    if imgOriginalScene is None:                            # if image was not read successfully
        print "\nerror: image not read from file \n\n"      # print error message to std out
        os.system("pause")                                  # pause so user can see error message
        return                                              # and exit program
    # end if

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)           # detect plates

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)        # detect chars in plates

    #cv2.imshow("imgOriginalScene", imgOriginalScene)            # show scene image

    if len(listOfPossiblePlates) == 0:                          # if no plates were found
        print "\nno license plates were detected\n"             # inform user no plates were found
    else:                                                       # else
                # if we get in here list of possible plates has at leat one plate

                # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)

                # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
        licPlate = listOfPossiblePlates[0]

        #cv2.imshow("imgPlate", licPlate.imgPlate)           # show crop of plate and threshold of plate
        #cv2.imshow("imgThresh", licPlate.imgThresh)

        if len(licPlate.strChars) == 0:                     # if no chars were found in the plate
            print "\nno characters were detected\n\n"       # show message
            return                                          # and exit program
        # end if

        drawRedRectangleAroundPlate(imgOriginalScene, licPlate)             # draw red rectangle around plate

        plaka =  licPlate.strChars

        print plaka
        if plaka[0].isalpha() :

            if plaka[0] == 'B':
                plaka = "0" + plaka[1:]

            elif plaka[0] == 'O' or plaka[0] == 'o':
                plaka = "0" + plaka[1:]
            elif plaka[0] == 'S':
                plaka = "5" + plaka[1:]
            elif plaka[0] == 'Z':
                plaka = "2" + plaka[1:]
            elif plaka[0] == 'I':
                plaka = "1" + plaka[1:]
            elif plaka[0] == 'U':
                plaka = "0" + plaka[1:]
            elif plaka[0] == 'G':
                plaka = "6" + plaka[1:]
            else:
                plaka = plaka[1:]

        if plaka[1].isalpha():

            if plaka[1] == 'B':
                plaka = plaka[0] + "0" + plaka[2:]

            elif plaka[1] == 'O' or plaka[0] == 'o':
                plaka = plaka[0] + "0" + plaka[2:]
            elif plaka[1] == 'S':
                plaka = plaka[0] + "5" + plaka[2:]
            elif plaka[1] == 'Z':
                plaka = plaka[0] + "2" + plaka[2:]
            elif plaka[1] == 'I':
                plaka = plaka[0] + "1" + plaka[2:]
            elif plaka[1] == 'U':
                plaka = plaka[0] + "0" + plaka[2:]
            elif plaka[1] == 'G':
                plaka = plaka[0] + "6" + plaka[2:]

        try:
            if plaka[2].isdigit():

                if plaka[2] == '1':
                    plaka = plaka[0] + plaka[1] + "T" + plaka[3:]
                if plaka[2] == '8':
                    plaka = plaka[0] + plaka[1] + "B" + plaka[3:]
        except:
            print "It cannot read"

        try:
            if plaka[3].isdigit():

                if plaka[3] == '1':
                    plaka = plaka[0:3] + "T" + plaka[4:]
                if plaka[3] == '8':
                    plaka = plaka[0:3] + "B" + plaka[4:]



        except:
            print "It cannot read"

        if plaka[-1].isalpha():

            if plaka[-1] == 'Z':
                plaka = plaka[0:-1] + "2"

            elif plaka[-1] == 'O':
                plaka = plaka[0:-1] + "0"

            elif plaka[-1] == 'B':
                plaka = plaka[0:-1] + "0"

            elif plaka[-1] == 'S':
                plaka = plaka[0:-1] + "5"

            elif plaka[-1] == 'I':
                plaka = plaka[0:-1] + "1"
            elif plaka[-1] == 'U':
                plaka = plaka[0:-1] + "0"
            else:
                plaka = plaka[0:-1]
                if plaka[-1].isalpha():

                    if plaka[-1] == 'Z':
                        plaka = plaka[0:-1] + "2"

                    elif plaka[-1] == 'O':
                        plaka = plaka[0:-1] + "0"

                    elif plaka[-1] == 'B':
                        plaka = plaka[0:-1] + "0"

                    elif plaka[-1] == 'S':
                        plaka = plaka[0:-1] + "5"

                    elif plaka[-1] == 'I':
                        plaka = plaka[0:-1] + "1"
                    elif plaka[-1] == 'U':
                        plaka = plaka[0:-1] + "0"


        try:
            if plaka[-2].isalpha():

                if plaka[-2] == 'Z':
                    plaka = plaka[0:-2] + "2" + plaka[-1]

                elif plaka[-2] == 'O':
                    plaka = plaka[0:-2] + "0" + plaka[-1]

                elif plaka[-2] == 'B':
                    plaka = plaka[0:-2] + "0" + plaka[-1]
                elif plaka[-2] == 'S':
                    plaka = plaka[0:-2] + "5" + plaka[-1]
                elif plaka[-2] == 'I':
                    plaka = plaka[0:-2] + "1" + plaka[-1]
                elif plaka[-2] == 'U':
                    plaka = plaka[0:-2] + "0" + plaka[-1]
        except:
            print "It cannot read"


        if len(plaka) > 6 and len(plaka) < 8:

            #try:

                con = sqlite3.connect("deneme.db")

                cursor = con.cursor()

                def create_table():
                    cursor.execute(
                        "CREATE TABLE IF NOT EXISTS plate (Plate_Number TEXT, Enter DOUBLE, Enter_Time TIMESTAMP, Exit DOUBLE, Exit_Time TIMESTAMP, Payment DOUBLE)")
                    con.commit()

                create_table()
                liste = list()



                cursor.execute("Select * From plate where Plate_Number = ?", (plaka,))

                liste = cursor.fetchone()

                print liste

                if liste != None:

                    simdi2 = float(str(time.time())[-9:])

                    now2 = datetime.datetime.now()

                    cursor.execute("Update plate set Exit = ?, Exit_Time = ? where Plate_Number = ? ",
                                   (simdi2, now2, plaka))
                    con.commit()

                    cursor.execute("Select * From plate where Plate_Number = ?", (plaka,))

                    liste = cursor.fetchone()

                    cost = liste[3] - liste[1]



                    if cost < 5.05:
                        finalCost = 5
                    elif cost < 10.05:
                        finalCost = 10
                    elif cost < 15.05:
                        finalCost = 15
                    else:
                        finalCost = 25

                    cursor.execute("Update plate set Payment = ? where Plate_Number = ?", (finalCost, plaka))
                    con.commit()

                    plate = liste[0]
                    checkin = liste[2]
                    checkout = liste[4]

                    file = open("Plates.txt", "a")
                    file.write(plaka + " " + checkin + " " + checkout + " " + str(finalCost) + "TL\n")
                    file.close()

                    print "Plaka : " + plate
                    print "Check-in Time : " + checkin[0:19]
                    print "Check-out Time : " + checkout[0:19]
                    print "Payment : ", finalCost, "TL"



                    time.sleep(1)

                    cursor.execute("Delete From plate where Plate_Number = ?",(plaka,))
                    con.commit()

                else:
                    simdi = float(str(time.time())[-9:])


                    now1 = datetime.datetime.now()

                    cursor.execute(
                        "INSERT INTO plate(Plate_Number,Enter,Enter_Time,Exit,Exit_Time,Payment) Values (?,?,?,?,?,?)",
                        (plaka, simdi, now1, "", "", ""))
                    con.commit()

                con.close()

            #except:
                #print "Database Error"

        else:
            print "Plaka Error"






        print "\nlicense plate read from image = " + plaka + "\n"       # write license plate text to std out

        print "----------------------------------------"

        writeLicensePlateCharsOnImage(imgOriginalScene, licPlate)           # write license plate text on the image

        #cv2.imshow("imgOriginalScene", imgOriginalScene)                # re-show scene image

        cv2.imwrite("imgOriginalScene.png", imgOriginalScene)           # write image out to file

    # end if else

    cv2.waitKey(0)					# hold windows open until user presses a key

    return
# end main

###################################################################################################
def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):

    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)            # get 4 vertices of rotated rect

    cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 2)         # draw 4 red lines
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 2)
# end function

###################################################################################################
def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
    ptCenterOfTextAreaX = 0                             # this will be the center of the area the text will be written to
    ptCenterOfTextAreaY = 0

    ptLowerLeftTextOriginX = 0                          # this will be the bottom left of the area that the text will be written to
    ptLowerLeftTextOriginY = 0

    sceneHeight, sceneWidth, sceneNumChannels = imgOriginalScene.shape
    plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape

    intFontFace = cv2.FONT_HERSHEY_SIMPLEX                      # choose a plain jane font
    fltFontScale = float(plateHeight) / 30.0                    # base font scale on height of plate area
    intFontThickness = int(round(fltFontScale * 1.5))           # base font thickness on font scale

    textSize, baseline = cv2.getTextSize(licPlate.strChars, intFontFace, fltFontScale, intFontThickness)        # call getTextSize

            # unpack roatated rect into center point, width and height, and angle
    ( (intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg ) = licPlate.rrLocationOfPlateInScene

    intPlateCenterX = int(intPlateCenterX)              # make sure center is an integer
    intPlateCenterY = int(intPlateCenterY)

    ptCenterOfTextAreaX = int(intPlateCenterX)         # the horizontal location of the text area is the same as the plate

    if intPlateCenterY < (sceneHeight * 0.75):                                                  # if the license plate is in the upper 3/4 of the image
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(round(plateHeight * 1.6))      # write the chars in below the plate
    else:                                                                                       # else if the license plate is in the lower 1/4 of the image
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(round(plateHeight * 1.6))      # write the chars in above the plate
    # end if

    textSizeWidth, textSizeHeight = textSize                # unpack text size width and height

    ptLowerLeftTextOriginX = int(ptCenterOfTextAreaX - (textSizeWidth / 2))           # calculate the lower left origin of the text area
    ptLowerLeftTextOriginY = int(ptCenterOfTextAreaY + (textSizeHeight / 2))          # based on the text area center, width, and height

            # write the text on the image
    cv2.putText(imgOriginalScene, licPlate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY), intFontFace, fltFontScale, SCALAR_YELLOW, intFontThickness)
# end function

###################################################################################################



#if __name__ == "__main__":
#    main()






















