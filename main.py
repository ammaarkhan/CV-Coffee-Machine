import os
from cvzone.HandTrackingModule import HandDetector
import cv2

cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread("Resources/Background.png")

# loading mode images
pathMode = "Resources/Modes"  # this is path to where the modes are saved
pathImgModes = os.listdir(pathMode)  # this saves the names of the files in a list
pathImgModes.sort()  # to get the correct order of file names
imgModes = []
for img in pathImgModes:
    imgModes.append(cv2.imread(os.path.join(pathMode, img)))
# print(imgModes)

# loading icon images
pathIcons = "Resources/Icons"  # this is path to where the modes are saved
pathImgIcons = os.listdir(pathIcons)  # this saves the names of the files in a list
pathImgIcons.sort()  # to get the correct order of file names
imgIcons = []
for icon in pathImgIcons:
    imgIcons.append(cv2.imread(os.path.join(pathIcons, icon)))

modeNum = 0  # to change the mode on the side
selection = -1  # for selection of menu item
counter = 0  # for time limit
circlePositions = [(1136, 196), (1000, 384), (1136, 581)]
counterPause = 0
selectionList = [-1, -1, -1]

detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    # this will overlay the camera feed on the background img
    imgBackground[139:139 + 480, 50:50 + 640] = img
    # this will overlay the mode on the background img
    imgBackground[0:0 + 720, 847:847 + 433] = imgModes[modeNum]

    if hands and counterPause == 0 and modeNum < 3:
        # Hand 1
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)
        print(fingers1)

        if fingers1 == [0, 1, 0, 0, 0]:
            if selection != 1:
                counter = 1
            selection = 1
        elif fingers1 == [0, 1, 1, 0, 0]:
            if selection != 2:
                counter = 1
            selection = 2
        elif fingers1 == [0, 1, 1, 1, 0]:
            if selection != 3:
                counter = 1
            selection = 3
        else:
            selection = -1
            counter = 0

        if counter > 0:
            counter += 1
            # print(counter)
            cv2.ellipse(imgBackground, circlePositions[selection - 1], (103, 103), 0, 0, counter * 8, (0, 255, 0), 20)

            if counter * 7 > 360:
                selectionList[modeNum] = selection
                modeNum += 1
                counter = 0
                selection = -1
                counterPause = 1

    # pausing after selection
    if counterPause > 0:
        counterPause += 1
        if counterPause > 30:
            counterPause = 0

    # adding selection item
    if selectionList[0] != -1:
        imgBackground[636:636 + 65, 133:133 + 65] = imgIcons[selectionList[0]-1]
    if selectionList[1] != -1:
        imgBackground[636:636 + 65, 340:340 + 65] = imgIcons[2+selectionList[1]]
    if selectionList[2] != -1:
        imgBackground[636:636 + 65, 542:542 + 65] = imgIcons[5+selectionList[2]]

    # displaying
    # cv2.imshow("Image", img)
    cv2.imshow("Background", imgBackground)
    cv2.waitKey(1)