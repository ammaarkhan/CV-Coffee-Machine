import os
from cvzone.HandTrackingModule import HandDetector
import cv2

cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread("Resources/Background.png")

pathMode = "Resources/Modes"  # this is path to where the modes are saved
pathImgModes = os.listdir(pathMode)  # this saves the names of the files in a list
pathImgModes.sort()  # to get the correct order of file names
imgModes = []
for img in pathImgModes:
    imgModes.append(cv2.imread(os.path.join(pathMode, img)))
# print(imgModes)

modeNum = 0  # to change the mode on the side

detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    # this will overlay the camera feed on the background img
    imgBackground[139:139+480, 50:50+640] = img
    # this will overlay the mode on the background img
    imgBackground[0:0+720, 847:847+433] = imgModes[modeNum]

    if hands:
        # Hand 1
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)
        print(fingers1)

    # displaying
    # cv2.imshow("Image", img)
    cv2.imshow("Background", imgBackground)
    cv2.waitKey(1)


