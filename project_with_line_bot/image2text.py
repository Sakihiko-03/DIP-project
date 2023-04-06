from utlis import *
from ColorPicker import *
import pytesseract
import cv2
import json

def empty(e):
    pass

# img_path = "test.jpg"
def image2text(img_path):
    hsv = detect_hsv(img_path)
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    # Step 1
    img = cv2.imread(img_path)

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
        # print(pytesseract.image_to_string(roi))
        #replace("\n","") for remove "\n"
        highlightedText.append(pytesseract.image_to_string(roi).replace("\n", ""))
        # highlightedText.append(pytesseract.image_to_string(roi).replace("\"", ""))
    #save text to file csv
    saveText(highlightedText)

    #json.dumps for change list to string
    #[1:-1] use text between first charater and last character
    return json.dumps(highlightedText)[1:-1]



