import cv2

cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread("Resources/Background.png")

while True:
    success, img = cap.read()
    # this will overlay the camera feed on the image
    imgBackground[139:139+480, 50:50+640] = img

    # displaying
    # cv2.imshow("Image", img)
    cv2.imshow("Background", imgBackground)
    cv2.waitKey(1)


