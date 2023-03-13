import numpy as np
import cv2
import math
import time

print(time.time())
# read image
img = cv2.imread("testImg.jpg")

# convert to grayscale
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# apply Gaussian Blur
#smoothed = cv2.GaussianBlur(gray, (0,0), sigmaX=9, sigmaY=9, borderType = cv2.BORDER_DEFAULT)
smoothed = cv2.bitwise_not(gray)

# do adaptive threshold on gray image
thresh = cv2.adaptiveThreshold(smoothed, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 65, 10)
#thresh = cv2.bitwise_not(thresh)

cv2.imshow("Threshold", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Set up the SimpleBlobdetector with default parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 0
params.maxThreshold = 256

# Filter by Area.
params.filterByArea = False
params.minArea = 30
params.maxArea = 10000

# Filter by Color (black=0)
params.filterByColor = True
params.blobColor = 0

# Filter by Circularity
params.filterByCircularity = False
params.minCircularity = 0.5
params.maxCircularity = 1


# Filter by Convexity
params.filterByConvexity = False
params.minConvexity = 0.5
params.maxConvexity = 1

# Filter by InertiaRatio
params.filterByInertia = False
params.minInertiaRatio = 0
params.maxInertiaRatio = 1

# Distance Between Blobs
params.minDistBetweenBlobs = 0

# Do detecting
detector = cv2.SimpleBlobDetector_create(params)

# Get keypoints
keypoints = detector.detect(thresh)

print(len(keypoints))
print('')

# Get keypoint locations and radius
for keypoint in keypoints:
   x = int(keypoint.pt[0])
   y = int(keypoint.pt[1])
   s = keypoint.size
   r = int(math.floor(s/2))
   print (x,y,r)
   #cv2.circle(img, (x, y), r, (0, 0, 255), 2)

# Draw blobs
blobs = cv2.drawKeypoints(thresh, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow("Keypoints", blobs)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(time.time())

# Save result
cv2.imwrite("particle_blobs.jpg", blobs)
