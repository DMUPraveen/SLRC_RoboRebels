import feature_extractor
import preprocessor

import matplotlib.pyplot as plt
import numpy as np

import cv2

def get_bearing(img):

    src = img

    otsu_thresh = preprocessor.applyOtsu(src)
    kSize = 25
    src = otsu_thresh

    blobs = preprocessor.extract_blob(src)
    largestBlob = preprocessor.getLblob(blobs)

    testy1 = largestBlob.lowerY
    testy2 = largestBlob.upperY
    testx1 = largestBlob.lowerX
    testx2 = largestBlob.upperX

    #raise a flag if the above reaches 

    #print(testx1, testx2, testy1, testy2)
    slice = preprocessor.make_copy(src,testy1, testy2, testx1, testx2)
    slice = preprocessor.blur(slice,kSize)
    outline = preprocessor.canny(slice)

    cv2.imshow('Edge Image', outline)
    cv2.waitKey()

    c_outline = np.copy(outline)

    error_factor = 4
    image_perimeter = np.where(c_outline>0)[0].shape[0]

    minPoints_in_long_line = int(image_perimeter*float((8-error_factor)/29))
    intersection_threshold_long = int(0.5*minPoints_in_long_line)
    max_gap_lines_long = int(0.9*minPoints_in_long_line)

    
    stem_lines, height= feature_extractor.openCV_houghlines(c_outline, r_res=1, theta_res=np.pi/180, int_thresh=intersection_threshold_long, \
                                    l=None, minPoint_line=minPoints_in_long_line, maxLine_gap=max_gap_lines_long)

    
    #print("Originally has %i lines"%(len(stem_lines)))

    #Filter most suitable lines
    bestFitStem = feature_extractor.removeDup_sortLen(stem_lines,0.1,10)[:2]
    # for line in bestFitStem:
    #     line.print_()

    headImg = preprocessor.drawLines(c_outline,bestFitStem[:2])
    
    c_headImg = np.copy(headImg)

    error_factor = 4
    minPoints_in_line_short = int(image_perimeter*float((5-error_factor)/29))
    intersection_threshold_short = int(0.5*minPoints_in_line_short)
    max_gap_lines_short = int(0.9*minPoints_in_line_short)

    #print(image_perimeter, minPoints_in_line_short, intersection_threshold_short, max_gap_lines_short)
    head_lines, height= feature_extractor.openCV_houghlines(c_headImg, r_res=1, theta_res=np.pi/180, int_thresh=intersection_threshold_short, \
                                    l=None, minPoint_line=minPoints_in_line_short, maxLine_gap=max_gap_lines_short)


    #Filter most suitable lines
    bestFitHead = feature_extractor.removeDup_sortLen(head_lines,0.1,10)
    
    # print("Originally has %i lines"%(len(head_lines)))
    # print("Now has ", len(bestFitHead))

    # for line in bestFitHead:
    #     line.print_()

    for i in range(len(bestFitHead)):
        for j in range(i+1, len(bestFitHead)):
            x = feature_extractor.intersects(outline.shape, bestFitHead[i], bestFitHead[j])
            if x[0]==True:
                vertex = x[1]
    midpoint = (bestFitStem[0].get_midpoint()+bestFitStem[1].get_midpoint())/2
    print(feature_extractor.bearing(midpoint[0],midpoint[1],vertex[0],vertex[1]))


if __name__ == '__main__':
    filename = 'samples/s1.jpg'
    src = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    get_bearing(src)