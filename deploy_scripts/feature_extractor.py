import numpy as np
import cv2
import math 

'''
openCV_houghlines():-->

dst: Output of the edge detector. It should be a grayscale image (although in fact it is a binary one)
lines: A vector that will store the parameters (xstart,ystart,xend,yend) of the detected lines
rho : The resolution of the parameter r in pixels. We use 1 pixel.
theta: The resolution of the parameter θ in radians. We use 1 degree (CV_PI/180)
threshold: The minimum number of intersections to "*detect*" a line
minLineLength: The minimum number of points that can form a line. Lines with less than this number of points are disregarded.
maxLineGap: The maximum gap between two points to be considered in the same line.

'''

class line():
    def __init__(self, vertex):
        self.vertex1 = np.array((vertex[0], vertex[1]))
        self.vertex2 = np.array((vertex[2], vertex[3]))

    def get_gradient(self):
        delta_xy = self.vertex2-self.vertex1
        return delta_xy[1]/delta_xy[0]

    def get_intercept(self):
        return self.vertex1[1] -self.gradient*self.vertex1[0]
        
    def get_length(self):
        return math.sqrt((self.vertex1-self.vertex2)**2)
    
    def get_midpoint(self):
        return (self.vertex1+self.vertex2)/2
    


def openCV_houghlines(mat,r_res=1,theta_res=np.pi / 180, int_thresh=50, l=None, minPoint_line=25, maxLine_gap=10,f= False):

    lines = []
    # Loads an image
    if f:
        src = cv2.imread(mat, cv2.IMREAD_GRAYSCALE)
    else:
        src = mat
    # Check if image is loaded fine
    if src is None:
        print ('Error opening image!')
        print ('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1

    linesP = cv2.HoughLinesP(src, r_res, theta_res, int_thresh, l, minPoint_line, maxLine_gap)
    h,_ = src.shape

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = np.copy(linesP[i][0])
            lineCls = line(np.array([l[0],h-l[1],l[2],h-l[3]]))
            lines.append(lineCls)
            cv2.line(src, (l[0], l[1]), (l[2], l[3]), (255,255,255), 3, cv2.LINE_AA)
    

    return lines, h

# get the equations of the lines
def get_lines(line_12):
    lines_out = []
    for i in range(len(line_12)):
        l = line_12[i][0]
        gradient = (l[-1]-l[1])/(l[-2]-l[0])
        intercept = (l[1])-gradient*l[0]
        lines_out.append((gradient, intercept))

    return lines_out


#get all the vertices of the arrow
def get_vertices(master_lines):
    vertices = []
    for i in range(len(master_lines)):
        l = master_lines[i][0]
        vertices.append(l.vertex1)
        vertices.append(l.vertex2)
    return list(set(vertices))

#get the distances to the lines
def get_distances(lines, vertices):
    distance = 0
    line_index = 0
    vert_index = 0
    for l_num in range(len(lines)):
        for p_num in range(len(vertices)):
            new_dis = get_dis(lines[l_num], vertices[p_num])
            if distance<new_dis:
                distance = new_dis
                line_index = l_num
                vert_index = p_num
    return (line_index, vert_index)


# get the distance to a line from a given point
def get_dis(l, p):
    dis = abs(p[1]-l[0]*p[0]-l[1])/(math.sqrt((1+(l[0])**2)))
    return dis

#feature 1
#given the lines gradient and the point get the direction
def get_arrow_vector(line, point, h):
    
    perp = -1/line[0]
    
    #line 2
    perp_line = (perp, point[1]-perp*point[0])

    # solve x
    x = (perp_line[1]-line[1]) / (line[0]-perp_line[0])
    y = line[0]*x + line[1]
    print(point, x, y)
    # get the vector 
    return bearing(x,y,point[0],point[1])
    # points , (x,y) 

#feature 2
#get the euclidean distance given two points
def getEuclid(s,e):
    return math.sqrt((s[0]-e[0])**2+(s[1]-e[1])**2)
    
def get_stem(svertices, long_vertices):
    # get the longest lines

    # find the vertex that is closest to the head 
    # pop the far vertices : possible validation step here to see if there is a line closer to those already
    # now ideally we should be left with three or less vertices
    pass

def bearing(start_x, start_y, end_x, end_y):
    delta_x = end_x - start_x
    delta_y = end_y - start_y
    radian_bearing = math.atan2(delta_y, delta_x)
    degree_bearing = math.degrees(radian_bearing)
    print("Deg ", degree_bearing)
    return (degree_bearing+360) % 360
    


if __name__ == "__main__":
    lines_points , height= openCV_houghlines('output.jpeg', f=True)
    
    lines_Eqns = get_lines(lines_points)
    vertices = get_vertices(lines_points)
    distances = get_distances(lines_Eqns, vertices)
    # print(lines_Eqns[distances[0]], vertices[distances[1]])
    dir_vector = get_arrow_vector(lines_Eqns[distances[0]], vertices[distances[1]], height)

    default_file = 'output.jpeg'
    src = cv2.imread(cv2.samples.findFile(default_file), cv2.IMREAD_GRAYSCALE)

    l = lines_points[distances[0]][0]
    print((l[0],height-l[1]),"&",(l[2],height-l[3]))
    cv2.line(src, (l[2],height-l[3]),(l[0],height-l[1]),  (255,255,255), 5, cv2.LINE_AA)
    cv2.line(src, (vertices[distances[1]][0], int(height-vertices[distances[1]][1])), ((l[0]+l[2])//2,  int(height-(l[1]+l[3]))//2), (255,255,255), 5, cv2.LINE_AA)
    cv2.imshow("Source", src)
    cv2.waitKey()
    print(dir_vector)




