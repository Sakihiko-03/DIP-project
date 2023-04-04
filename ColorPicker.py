import cv2
import numpy as np


def detect_hsv(img_path):
    # Load image
    img = cv2.imread(img_path)

    # Resize image
    img = cv2.resize(img, (0, 0), None, 0.5, 0.5)

    # Convert image to HSV color space
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow("mask", hsv_img)

    # Define color ranges to detect
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])

    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 30])

    # Mask for black and white regions
    white_mask = cv2.inRange(hsv_img, lower_white, upper_white)
    black_mask = cv2.inRange(hsv_img, lower_black, upper_black)
    mask = cv2.bitwise_or(white_mask, black_mask)
    cv2.imshow("mask", mask)

    # Invert mask to detect other colors
    mask = cv2.bitwise_not(mask)
    cv2.imshow("mask", mask)

    # Apply mask to image
    color_img = cv2.bitwise_and(hsv_img, hsv_img, mask=mask)
    cv2.imshow("mask", color_img)

    # Find the most common color in the image
    h, s, v = cv2.split(color_img)
    hist = cv2.calcHist([h], [0], mask, [180], [0, 180])
    color_hue = int(hist.argmax())

    # Calculate lower and upper bounds of color range
    lower_color = np.array([color_hue - 10, 50, 50])
    upper_color = np.array([color_hue + 10, 255, 255])

    # Print lower and upper bounds of color range
    print("Lower Bound: ", lower_color)
    print("Upper Bound: ", upper_color)

    # Return color in HSV color space
    color = np.concatenate((lower_color, upper_color)).tolist()
    hsv = [color[i] for i in [0, 3, 1, 4, 2, 5]]

    return hsv
