import numpy as np
import cv2 as cv
im = cv.imread('testImg.jpg')
assert im is not None, "file could not be read, check with os.path.exists()"
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# Draw all contours
# -1 signifies drawing all contours
cv.drawContours(im, contours, -1, (0, 255, 0), 3)
print(contours)  
cv.imshow('Contours', ret)
cv.waitKey(0)
cv.destroyAllWindows()
