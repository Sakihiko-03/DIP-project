import cv2
import numpy as np


def detectColor(img, hsv):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    reimgHSV = cv2.resize(imgHSV, (0, 0), None, 0.5, 0.5)
    cv2.imshow("hsv", reimgHSV)
    lower = np.array([hsv[0], hsv[2], hsv[4]])
    upper = np.array([hsv[1], hsv[3], hsv[5]])
    mask = cv2.inRange(imgHSV, lower, upper)
    remask = cv2.resize(mask, (0, 0), None, 0.5, 0.5)
    cv2.imshow("mask2", remask)
    imgResult = cv2.bitwise_and(img, img, mask=mask)
    reimgResult = cv2.resize(imgResult, (0, 0), None, 0.5, 0.5)
    cv2.imshow("imgResult", reimgResult)
    return imgResult


def getContours(img, imgDraw, cThr=[100, 100], showCanny=False, minArea=1000, filter=0, draw=False):
    imgDraw = imgDraw.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, cThr[0], cThr[1])
    kernal = np.array((10, 10))
    imgDial = cv2.dilate(imgCanny, kernal, iterations=1)
    imgClose = cv2.morphologyEx(imgDial, cv2.MORPH_CLOSE, kernal)

    if showCanny: cv2.imshow("Canny", imgClose)
    #imgGray or imgCanny
    contours, _ = cv2.findContours(imgGray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    finalCountours = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > minArea:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            bbox = cv2.boundingRect(i)
            bbox = [bbox[0], bbox[1] - 10, bbox[2], bbox[3] + 10]
            if filter > 0:
                if len(approx) == filter:
                    finalCountours.append([len(approx), area, approx, bbox, i])
            else:
                finalCountours.append([len(approx), area, approx, bbox, i])
    finalCountours = list(reversed(finalCountours))
    if draw:
        for con in finalCountours:
            x, y, w, h = con[3]
            # w += 5
            cv2.rectangle(imgDraw, (x, y), (x + w, y + h), (0, 0, 255), 3)
            # cv2.drawContours(imgDraw, con[4], -1, (0, 0, 255), 2)
    return imgDraw, finalCountours


def getRoi(img, contours):
    roiList = []
    for con in contours:
        x, y, w, h = con[3]
        # w += 5
        roiList.append(img[y:y + h, x:x + w])
    return roiList


def roiDisplay(roiList):
    for x, roi in enumerate(roiList):
        roi = cv2.resize(roi, (0, 0), None, 1, 1)
        # cv2.namedWindow(str(x), cv2.WINDOW_AUTOSIZE)
        cv2.imshow(str(x), roi)


def saveText(highlightedText):
    with open('HighlightedText.csv', 'w') as f:
        for text in highlightedText:
            f.writelines(f'\n{text}')

