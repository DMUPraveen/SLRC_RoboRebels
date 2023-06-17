from feature_extractor import *
from preprocessor import *

import matplotlib.pyplot as plt
import numpy as np

def plot_lines_and_points(lines, points):
    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Plot each line
    for line in lines:
        # Get the gradient and intercept values
        m, c = line

        # Generate x values
        x = np.linspace(0, 10, 100)

        # Calculate corresponding y values
        y = m * x + c

        # Plot the line
        ax.plot(x, y)

    # Plot each point
    for point in points:
        # Get the x and y values
        x, y = point

        # Plot the point
        ax.scatter(x, y, marker='o', color='red')

    # Add labels and a grid
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.grid(True)

    # Show the plot
    plt.show()

if __name__=='__main__':

    filename = 's1.jpg'
    src = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    otsu_thresh = applyOtsu(src)

    src = otsu_thresh
    blobs = extract_blob(src)
    largestBlob = getLblob(blobs)
    testy1 = largestBlob.lowerY
    testy2 = largestBlob.upperY

    testx1 = largestBlob.lowerX
    testx2 = largestBlob.upperX
    #print(testx1, testx2, testy1, testy2)
    slice = make_copy(src,testy1, testy2, testx1, testx2)
    outline = simpleEdge(otsu_thresh)

    cv2.imshow('Edge Image', outline)
    cv2.waitKey()

    lines_points , height= openCV_houghlines(outline)
    #print(lines_points)
    lines_Eqns = get_lines(lines_points)
    
    vertices = get_vertices(lines_points)
    distances = get_distances(lines_Eqns, vertices)
    dir_vector = get_arrow_vector(lines_Eqns[distances[0]], vertices[distances[1]], height)
    
    l = lines_points[distances[0]][0]
    cv2.line(outline, (l[0],l[1]), (l[2],l[3]), (255,255,255), 5, cv2.LINE_AA)
    cv2.line(outline, (vertices[distances[1]][0], vertices[distances[1]][1]), ((l[0]+l[2])//2,  (l[1]+l[3])//2), (255,255,255), 5, cv2.LINE_AA)
    cv2.imshow("Source", outline)
    cv2.waitKey()
    print(dir_vector)
