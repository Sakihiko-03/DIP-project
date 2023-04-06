from utlis import *
from ColorPicker import *
import pytesseract
import cv2


def empty(e):
    pass


hsv = detect_hsv('dip4.jpg')
print(hsv)
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'


# Step 1
img = cv2.imread('dip4.jpg')

# Step 2
imgResult = detectColor(img, hsv)

# Step 3 & 4
imgContours, contours = getContours(imgResult, img, showCanny=True,
                                    minArea=1000, filter=0,
                                    cThr=[100, 150], draw=True)
imgContours = cv2.resize(imgContours, (0, 0), None, 0.5, 0.5)
cv2.imshow("imgContours", imgContours)
print(len(contours))

# Step 5
roiList = getRoi(img, contours)
roiDisplay(roiList)

# Step 6
highlightedText = []
for x, roi in enumerate(roiList):
    print(pytesseract.image_to_string(roi))
    # highlightedText.append(pytesseract.image_to_string(roi))
    highlightedText.append(pytesseract.image_to_string(roi).replace("\n", ""))
saveText(highlightedText)


cv2.waitKey(0)
