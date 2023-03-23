import feature_extractor
import preprocessor

import matplotlib.pyplot as plt
import numpy as np

import cv2

# Area Threshold for predicting not arrow (See Heuristic #2)
#TODO: Tune me
notArrow_areaThres = 3000
notArrow_areaThres_lower = 250
stemLongLineNum_thresh = 8
waitkey_delay = 32

def raiseFlag(code,v):
    flags = ['Spans Entire Height.Not Arrow',\
             'Spans Entire Width.Not Arrow',\
             'Area of the blob is too big.Reduced Confidence and moving on...',\
             'Increasing Stem Error Factor..Confidence Reduced..',\
             'Stem Lines not detected successfully.Moving to next blob..',\
             'Detected More than %i Lines in Stem.Reduced confidence and moving on...'%(stemLongLineNum_thresh),
             'Couldn\'t Find enough short lines. Reducing short lines error_factor. Reduced COnfidence and continuing',\
             'Failed to extract head. Trying the next blob',\
             'Arrow not found. Exiting...',\
             'Too small to be an arrow']
    if v==True:
        print(flags[code])

def get_bearing(img,verbose=False, imgVerbose=False):

    #Extract Image data
    src = img
    verbImage = np.copy(src)
    verbImage = cv2.cvtColor(verbImage, cv2.COLOR_GRAY2BGR)

    #print('Imasge size ',src.shape)
    # Apply Otsu Thresholding to the Entire Image
    otsu_thresh = preprocessor.applyOtsu(src)
    kSize = 25
    src = otsu_thresh
    if imgVerbose:
        cv2.imshow("Otsu Thresholding", src)
        cv2.waitKey(waitkey_delay)

    # Extract the white blobs on the Image
    blobs = preprocessor.extract_blob(src)
    arrowFound = False

    verbImage_blob = np.copy(verbImage)
    if imgVerbose:
        for b in blobs:
            cv2.rectangle(verbImage_blob, (b.lowerX, b.lowerY), (b.upperX, b.upperY), (0,0,255), thickness=2)
        cv2.imshow("Detected Blobs ",verbImage_blob)
        cv2.waitKey(32)

    # Iterate through the blobs starting largest first until arrow feature are detected
    while (arrowFound==False):
        confidence = 1
        # Take the largest blob and find it extents
        height, width_ = src.shape
        
        largestBlob = preprocessor.getLblob(blobs)
        if largestBlob=='f':
            return -1, -1
        testy1 = largestBlob.lowerY
        testy2 = largestBlob.upperY
        testx1 = largestBlob.lowerX
        testx2 = largestBlob.upperX
        #print('a',testx1, testx2, testy1, testy2,src.shape)

        # Heuristic #0 : Checks if the blob extends across the entire \
        #                image end to end and skips to the next blob
        if testy2-testy1>height:
            # Raise Flag 0 - Blob extends across entire Height. Can't be an arrow
            raiseFlag(0, verbose)

            if len(blobs)>0:
                blobs.remove(largestBlob)
                continue
            else:
                raiseFlag(8,verbose)
                arrowFound = False

            continue
        if testx2-testx1>width_:
            # Raise Flag 0 - Blob extends across entire Width. Can't be an arrow
            raiseFlag(1, verbose)

            if len(blobs)>0:
                blobs.remove(largestBlob)
                continue
            else:
                raiseFlag(8,verbose)
                arrowFound = False

            continue       
        
        # Heuristic #1 : If blob area is too large reduce confidence\
        #                Needs tuning. Not definitive
        if verbose:
            print('Area of the current blob',largestBlob.area(),end='\t')
        if largestBlob.area()>notArrow_areaThres:
            raiseFlag(2, verbose)
            cv2.rectangle(verbImage, (testx1, testy1), (testx2, testy2), (0,0,255), thickness=2)
            confidence-=0.3
        elif largestBlob.area()<notArrow_areaThres_lower:
            raiseFlag(9, verbose)
            blobs.clear()
            break
                   

        #print((testy1, testy2, testx1, testx2))
        #Blur the image to remove aliasing and then apply Canny Edge Detector
        slice = preprocessor.make_copy(src,testy1, testy2, testx1, testx2)
        slice = preprocessor.blur(slice,kSize)
        outline = preprocessor.canny(slice)

        # Display Outline of the Image
        # cv2.imshow('Edge Image', outline)
        # cv2.waitKey(32)


        # Get the longest line you can fit into this outline you've got
        # Hough Transform parameters are a funtion of the perimeter of the arrow detected 
        # Taken considering ratios of the actual arror standard

        stemFound = False
        error_factor = 4               # Higher the error Factor, shorter the lines detected
        if verbose:
            print("Finding Stem")
        while not(stemFound) and error_factor<8:
            
            c_outline = np.copy(outline)
            image_perimeter = np.where(c_outline>0)[0].shape[0]
            minPoints_in_long_line = int(image_perimeter*float((8-error_factor)/29))
            intersection_threshold_long = int(0.5*minPoints_in_long_line)
            max_gap_lines_long = int(0.9*minPoints_in_long_line)

            stem_lines, height= feature_extractor.openCV_houghlines(c_outline, r_res=1, theta_res=np.pi/180, int_thresh=intersection_threshold_long, \
                                            l=None, minPoint_line=minPoints_in_long_line, maxLine_gap=max_gap_lines_long)
            

            # **--Metadata--**
            #print("Originally has %i lines"%(len(stem_lines)))
            #Filter most suitable lines by removing near parallel lines 
            bestFitStem = feature_extractor.removeDup_sortLen(stem_lines,0.1,10)
            if len(bestFitStem)<2:
                #print(len(stem_lines))
                raiseFlag(3,verbose)
                confidence-=0.2*(error_factor/8)
                error_factor+=1
            else:
                stemFound = True

        if not(stemFound):
            raiseFlag(4,verbose)

            if len(blobs)>0:
                blobs.remove(largestBlob)
                
            else:
                raiseFlag(8,verbose)
                arrowFound = False
            continue
        if verbose:
            print("Found Stem")
        # Heuristic #2 : If long lines to having more than 2 lines, its more likely that we are looking at something 
        #                other than an arrow. Reduce confidence here
        if len(bestFitStem)>stemLongLineNum_thresh:
            raiseFlag(5, verbose)
            confidence-=0.1
        bestFitStem = bestFitStem[:2]

        # for line in bestFitStem:
        #     line.print_()

        # Draw lines over the supposedly detected stem and leave onlt the arrow head and base of the stem
        headFound = False
        error_factor = 3
        previous_error_factor = error_factor
        if verbose:
            print("Finding Head")

        while not(headFound) and error_factor<5:
            headImg = preprocessor.drawLines(outline,bestFitStem[:2])
            c_headImg = np.copy(headImg)
            minPoints_in_line_short = int(image_perimeter*float((5-error_factor)/29))
            intersection_threshold_short = int(0.5*minPoints_in_line_short)
            max_gap_lines_short = int(0.9*minPoints_in_line_short)


            #print(image_perimeter, minPoints_in_line_short, intersection_threshold_short, max_gap_lines_short)
            head_lines, height= feature_extractor.openCV_houghlines(c_headImg, r_res=1, theta_res=np.pi/180, int_thresh=intersection_threshold_short, \
                                            l=None, minPoint_line=minPoints_in_line_short, maxLine_gap=max_gap_lines_short)
        
            if imgVerbose:
                #print('Error Factor ', error_factor)
                cv2.imshow('Short Lines Input', headImg)
                cv2.imshow('Short Lines Output', c_headImg)
                cv2.waitKey(waitkey_delay)

            
            # Reduce the error factor ratio till sufficient lines are found

            #Filter most suitable lines by removing duplicates
            bestFitHead = feature_extractor.removeDup_sortLen(head_lines,0.15,10)
            if verbose and imgVerbose:
                print('Error Factor %i \t Got %i lines and cleaned to get %i'%(error_factor, len(head_lines),len(bestFitHead)))

            if len(bestFitHead)<=2:
                raiseFlag(6,verbose)
                confidence-=0.15*(error_factor/6)
                error_factor+=1
                continue
           
            #TODO : What if all three lines aren't found?\
            #        Guessing that all three parts are found for now


            
            # print("Originally has %i lines"%(len(head_lines)))
            # print("Now has ", len(bestFitHead))

            # for line in bestFitHead:
            #     line.print_()

            # Run Heuristics for the arrow head's lines

            # Heuristic #3 : Lines intersect inside image bounds
            for i in range(len(bestFitHead)):
                for j in range(i+1, len(bestFitHead)):
                    x = feature_extractor.intersects(outline.shape, bestFitHead[i], bestFitHead[j])
                    if x[0]==True:
                        # TODO: Check if this vertex is close one vertex of each line that youve got, If so it checks out ...Else 
                        isCloseInt = feature_extractor.intersection_in_head(bestFitHead[i], bestFitHead[j], x[1])
                        if imgVerbose and verbose:
                            print('Posible Intersection found at (%i,%i)'%(x[1][0],x[1][1]))
                            bestFitHead[i].print_()
                            bestFitHead[j].print_()
                            print("Is close?\t",isCloseInt)
                        if isCloseInt:
                            vertex = x[1]
                            headFound = True
                            break
            if verbose:
                print('Error Factor %i \t Head Found Status %s'%(error_factor, str(headFound)))
            if error_factor==4 and not(headFound):
                break
            
            elif previous_error_factor==error_factor:
                previous_error_factor = error_factor
                error_factor +=1
                confidence-=0.1
            

            #TODO : Implement a function to calculate the distance between the given vertices and validate

        if not(headFound):
            raiseFlag(7,verbose)

            if len(blobs)>0:
                blobs.remove(largestBlob)
                continue
            else:
                raiseFlag(8,verbose)
                arrowFound = False

            break
        if verbose:
            print("Found Head")

        #DONE : Implement mechanism to see if arrow actually found # Send image to webots window overlay
        if confidence>0.5:
            arrowFound = True
            
        if len(bestFitStem)>=2:
            midpoint = (bestFitStem[0].get_midpoint()+bestFitStem[1].get_midpoint())/2


    if arrowFound:
        heading_towards = feature_extractor.bearing(midpoint[0],midpoint[1],vertex[0],vertex[1])
        stemCenter = (midpoint[0]//1,midpoint[1]//1)
        if verbose:
            print('Found Arrow with confidence %2.3f'%(confidence),'\t',end='', flush=True)
            print((midpoint[0]//1,midpoint[1]//1),(vertex[0]//1,vertex[1]//1), flush=True)

        if imgVerbose:
            cv2.circle(verbImage, (testx1+int(midpoint[0]),testy1+height-int(midpoint[1])), 3, (0, 0, 255), -1)
            cv2.circle(verbImage, (testx1+int(vertex[0]),testy1+height-int(vertex[1])), 3, (255, 0, 0), -1)
            cv2.rectangle(verbImage, (testx1, testy1), (testx2, testy2), (0,255,0), thickness=2) #TODO: put me inside verbose later 
            cv2.imshow("Verbose Image", verbImage)
            cv2.waitKey(waitkey_delay)

        return confidence, heading_towards
    else:
        if imgVerbose:
            cv2.rectangle(verbImage, (testx1, testy1), (testx2, testy2), (0,0,255), thickness=2)
            cv2.imshow("Verbose Image", verbImage)
            cv2.waitKey(waitkey_delay)

        if len(blobs)>0:
            blobs.remove(largestBlob)
        else:
            raiseFlag(8,verbose)
            
        return -1,-1
            
        
def get_closest_blob_coord(img, imgVerb = False):
    #Extract Image data
    src = img

    #print('Imasge size ',src.shape)
    # Apply Otsu Thresholding to the Entire Image
    otsu_thresh = preprocessor.applyOtsu(src)
    kSize = 25
    src = otsu_thresh

    # Extract the white blobs on the Image
    blobs = preprocessor.extract_blob(src)
    clipped = False

    if len(blobs)>1:
        tb = preprocessor.getLblob(blobs)
        if tb.upperX>=img.shape[1]-1 or tb.upperY>=img.shape[0]-1:
            clipped = True
    elif len(blobs)==1:
        tb = blobs[0]
        if tb.upperX>=img.shape[1]-1 or tb.upperY>=img.shape[0]-1:
            clipped = True
    else:
        return False, -1, -1
    # testy1 = tb.lowerY
    # testy2 = tb.upperY
    # testx1 = tb.lowerX
    # testx2 = tb.upperX
    # print((testx1, testy1), (testx2, testy2), img.shape)
    # cv2.rectangle(img, (testx1, testy1), (testx2, testy2), (255,255,255), thickness=2)
    # cv2.imshow('Image', img)
    # cv2.waitKey(0)

    return True, tb, clipped



if __name__ == '__main__':
    filename = 'E:\\DEEE\\4th SEM\\SLRC 23\\root\\error_images\\errorImg3_1.jpg'
    src = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    #get_bearing(src,verbose=True, imgVerbose=True)
    print(get_closest_blob_coord(src))