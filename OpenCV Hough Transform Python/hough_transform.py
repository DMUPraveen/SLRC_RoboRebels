"""
@file hough_lines.py
@brief This program demonstrates line finding with the Hough transform
"""
import sys
import math
import cv2 as cv
import numpy as np 
def main(argv):
    
    default_file = 'output3.jpeg'
    filename = argv[0] if len(argv) > 0 else default_file
    # Loads an image
    src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_GRAYSCALE)
    # Check if image is loaded fine
    if src is None:
        print ('Error opening image!')
        print ('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1
    
    
    dst = cv.Canny(src, 50, 200, None, 3)
    
    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)
    
    lines = cv.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
    
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv.line(cdst, pt1, pt2, (0,0,255), 3, cv.LINE_AA)
    
    
    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)
    
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv.LINE_AA)
    
    cv.imshow("Source", src)
    cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
    cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)
    cv.waitKey()
    print(linesP, src.shape[1])
    return linesP, src.shape[1]
    

# get the equations of the lines
def get_lines(line_12):
    lines_out = []
    for i in range(len(line_12)):
        l = line_12[i][0]
        gradient = (l[-1]-l[1])/(l[-2]-l[0])
        intercept = l[1]-gradient*l[0]
        lines_out.append((gradient, intercept))

    return lines_out

#get all the vertices of the arrow
def get_vertices(master_points):
    vertices = []
    for i in range(len(master_points)):
        l = master_points[i][0]
        vertices.append((l[0], l[1]))
        vertices.append((l[-2], l[-1]))
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

            

# get the distance to a line
def get_dis(l, p):
    dis = abs(p[1]-l[0]*p[0]-l[1])/(math.sqrt((1+(l[0])**2)))
    return dis

#given the lines gradient and the point get the direction
def get_arrow_vector(line, point, h):
    perp = -1/line[0]
    
    #line 2
    perp_line = (perp, point[1]-perp*point[0])
    
    # solve x
    x = (perp_line[1]-line[1]) / (line[0]-perp_line[0])
    y = line[0]*x + line[1]
    # get the vector 
    return bearing(x,y,point[0],point[1])
    # points , (x,y) 

def bearing(start_x, start_y, end_x, end_y):
    delta_x = end_x - start_x
    delta_y = -end_y + start_y
    radian_bearing = math.atan2(delta_y, delta_x)
    degree_bearing = math.degrees(radian_bearing)
    return (degree_bearing + 360) % 360
    



if __name__ == "__main__":
    lines_points , height= main(sys.argv[1:])
    
    lines_Eqns = get_lines(lines_points)
    vertices = get_vertices(lines_points)
    distances = get_distances(lines_Eqns, vertices)
    print(lines_Eqns[distances[0]], vertices[distances[1]])
    dir_vector = get_arrow_vector(lines_Eqns[distances[0]], vertices[distances[1]], height)

    default_file = 'output3.jpeg'
    src = cv.imread(cv.samples.findFile(default_file), cv.IMREAD_GRAYSCALE)
    
    l = lines_points[distances[0]][0]
    cv.line(src, (l[0],l[1]), (l[2],l[3]), (255,255,255), 5, cv.LINE_AA)
    cv.line(src, (vertices[distances[1]][0], vertices[distances[1]][1]), ((l[0]+l[2])//2,  (l[1]+l[3])//2), (255,255,255), 5, cv.LINE_AA)
    cv.imshow("Source", src)
    cv.waitKey()
    print(dir_vector)

