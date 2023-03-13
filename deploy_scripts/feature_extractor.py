import numpy as np
import cv2
import math 

def openCV_houghlines(mat,r_res=1,theta_res=np.pi / 180, int_thresh=50, l=None, minPoint_line=25, maxLine_gap=10,f= False):
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
    
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(src, (l[0], l[1]), (l[2], l[3]), (255,255,255), 3, cv2.LINE_AA)
    

    return linesP, src.shape[1]


def my_houghlines():
    pass


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
    lines_points , height= openCV_houghlines('output.jpeg', True)
    
    lines_Eqns = get_lines(lines_points)
    vertices = get_vertices(lines_points)
    distances = get_distances(lines_Eqns, vertices)
    print(lines_Eqns[distances[0]], vertices[distances[1]])
    dir_vector = get_arrow_vector(lines_Eqns[distances[0]], vertices[distances[1]], height)

    default_file = 'output.jpeg'
    src = cv2.imread(cv2.samples.findFile(default_file), cv2.IMREAD_GRAYSCALE)
    
    l = lines_points[distances[0]][0]
    cv2.line(src, (l[0],l[1]), (l[2],l[3]), (255,255,255), 5, cv2.LINE_AA)
    cv2.line(src, (vertices[distances[1]][0], vertices[distances[1]][1]), ((l[0]+l[2])//2,  (l[1]+l[3])//2), (255,255,255), 5, cv2.LINE_AA)
    cv2.imshow("Source", src)
    cv2.waitKey()
    print(dir_vector)




