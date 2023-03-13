import cv2

# read image
img = cv2.imread("testImg.jpg")
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

class particle():
    def init(self,x, y):
        self.x = x
        self.y = y


class blob():
    def __init__(self, x, y):
        self.elements = set()
        self.neighbours = set()
        self.add_element(x, y)
    def add_element(self, x,y):
        if len(self.elements)==0 or self.in_neighbours(x,y):
            self.elements.add((x,y))
            
            self.neighbours.add((x-1,y-1))
            self.neighbours.add((x-1,y))
            self.neighbours.add((x-1,y+1))
            
            self.neighbours.add((x,y-1))
            self.neighbours.add((x,y+1))
            
            self.neighbours.add((x+1,y-1))
            self.neighbours.add((x+1,y))
            self.neighbours.add((x+1,y+1))
            return 1
        return 0
            
    def in_neighbours(self, x,y):
         if (x,y) in self.neighbours:
             return True
         return False

# get white pixel

# create blobs
# get area of the blobs
# draw bounding boxes using extremities

blobs = []

print(gray.shape)
h, w = gray.shape[0], gray.shape[1]

for y in range(h):
    for x in range(w):
        
        intensity = 0
        if gray[y, x]>100:
            intensity = 255
            
        if intensity ==255:
            added = 0
            for b in blobs:
                added = b.add_element(x,y)
                if added:
                    break
            if not(added):
                blobs.append(blob(x,y))
"""
for list(b.elements)[0] in blobs:
   gray = cv2.circle(gray, (x,y), radius=5, color=(0, 0, 255), thickness=-1)
   print(x,y)
"""

print(len(blobs))
cv2.imshow("Gray", gray)
cv2.waitKey()
