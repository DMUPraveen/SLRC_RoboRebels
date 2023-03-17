import cv2
import numpy as np

neighbourRadius = 25
class blob():
    def __init__(self, x, y,imgShape=(320,480)):
        self.elements = set()
        self.neighbours = set()
        self.edges = set()
        self.imgShape = imgShape
        if y<=self.imgShape[0]-(neighbourRadius+1):
            self.upperY = y+neighbourRadius
        else:
            self.upperY = self.imgShape[0]

        if y>=neighbourRadius:
            self.lowerY = y-neighbourRadius
        else:
            self.lowerY = 0 

        if x<=self.imgShape[1]-(neighbourRadius+1):
            self.upperX = x+neighbourRadius
        else:
            self.upperX = self.imgShape[1]

        if x>=neighbourRadius:
            self.lowerX = x-neighbourRadius
        else:
            self.lowerX = 0    

        #clip to image shape if exceeded

        self.add_element(x, y)
        self.last_element = (x,y)


    def add_element(self, x,y, is_edge=False):
        if len(self.elements)==0 or self.in_neighbours(x,y):
            self.elements.add((x,y))
            
            if abs(self.upperY-y)<neighbourRadius:
                if y<=self.imgShape[0]-(neighbourRadius+1):
                    self.upperY = y+neighbourRadius
                else:
                    self.upperY = self.imgShape[0]

            if abs(y - self.lowerY)<neighbourRadius:
                if y>=neighbourRadius:
                    self.lowerY = y-neighbourRadius
                else:
                    self.lowerY = 0 

            if abs(self.upperX-x)<neighbourRadius:
                if x<=self.imgShape[1]-(neighbourRadius+1):
                    self.upperX = x+neighbourRadius
                else:
                    self.upperX = self.imgShape[1]

            if abs(x - self.lowerX)<neighbourRadius:
                if x>=neighbourRadius:
                    self.lowerX = x-neighbourRadius
                else:
                    self.lowerX = 0
            
            if is_edge:
               self.add_to_edges(x,y)

            self.last_element = (x,y)
            
            return 1
        return 0
    
    def last2edge(self):
       self.add_to_edge(self.last_element)

    def add_to_edges(self,x,y):
       self.edges.add((x,y))
            
    def in_neighbours(self, x,y):
         if (x<self.upperX and x>self.lowerX) and (self.lowerY<y and self.upperY>y):
             return True
         
         return False
    
    def area(self):
      return len(self.elements)


def drawLines(img, lines):
    src = np.copy(img)
    for i in lines:
        cv2.line(src, (i.vertex1[0],img.shape[0]-i.vertex1[1]), (i.vertex2[0],img.shape[0]-i.vertex2[1]), (0,0,0), 3, cv2.LINE_AA)
    return src

    
# get white pixel
# create blobs
# get area of the blobs
# draw bounding boxes using extremities
def extract_blob(gray):
    blobs = []
    h, w = gray.shape[0], gray.shape[1]
    for y in range(h):
        for x in range(w):
            intensity = 0
            if gray[y, x]>15:
                intensity = 255
            if intensity ==255:
                added = 0
                for b in blobs:
                    added = b.add_element(x,y)
                    if added:
                        break
                if not(added):
                    blobs.append(blob(x,y))
    return blobs

def blur(img,kSize):
    return cv2.GaussianBlur(img,(kSize,kSize),0)

def canny(img):
    return cv2.Canny(img, 50, 200, None, 3)

def make_copy(src, yStart, yEnd, xStart, xEnd):
    import copy
    return copy.deepcopy(src[yStart:yEnd, xStart:xEnd])


def simpleEdge(inImg):
    # Define a kernel for detecting edges
    kernel = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]
    
    # Define the size of the image
    height = len(inImg)
    width = len(inImg[0])
    
    # Create a new image to hold the edge detection result
    result = [[0 for x in range(width)] for y in range(height)]
    
    # Iterate over the image pixels
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            # Apply the kernel to the pixel and its neighbors
            sum = 0
            for ky in range(3):
                for kx in range(3):
                    px = x + (kx - 1)
                    py = y + (ky - 1)
                    sum += inImg[py][px] * kernel[ky][kx]
        
            # Set the result pixel based on the kernel sum
        
            if sum > 255:
                result[y][x] = 255
    
    # Return the result image
    return np.array(result).astype('uint8')


def getLblob(blobs):
    largestIndex = 0
    largestSize = 0
    for b in range(len(blobs)):
        x = blobs[b].area()
        if x>largestSize:
            largestSize = x
            largestIndex = b
    return blobs[largestIndex]

def applyOtsu(img):
    _, threshImg = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return threshImg


if __name__== "__main__":

    filename = 'samples/s8.jpg'
    src = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

    verbImage = np.copy(src)
    verbImage = cv2.cvtColor(verbImage, cv2.COLOR_GRAY2BGR)
    height, width = src.shape

    # Apply Otsu Thresholding to the Entire Image
    otsu_thresh = applyOtsu(src)
    kSize = 25
    src = otsu_thresh

    blobs = extract_blob(src)
    """
    largestBlob = getLblob(blobs)

    testy1 = largestBlob.lowerY
    testy2 = largestBlob.upperY

    testx1 = largestBlob.lowerX
    testx2 = largestBlob.upperX

    slice = make_copy(src,testy1, testy2, testx1, testx2)

    outline = simpleEdge(slice)
    """
    for b in blobs:
        cv2.rectangle(verbImage, (b.lowerX, b.lowerY), (b.upperX, b.upperY), (0,0,255), thickness=2)
    cv2.imshow("sliced portion ",verbImage)
    cv2.waitKey()
    pass
