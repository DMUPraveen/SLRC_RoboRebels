from ab import moveForward, turnLeft, turnRight, stop
from sensors import ultrasonicReading
from dist import rightDistSensor, LeftDistSensor
from IRsensor import finishLineDitected

obsWidth = 5 #Assign the value
ultrasonicStatus = False

if ultrasonicReading < 1:
    ultrasonicStatus = True  #True if detects an obstacle

def obsAvoidAlgo():
    while ultrasonicStatus == False and finishLineDitected == False :
        moveForward()

    if ultrasonicStatus == True:
        if rightDistSensor < LeftDistSensor:
            turnLeft()
            distToWall = ultrasonicReading
            while distToWall - ultrasonicReading < 0.06:
                moveForward()

            turnRight()
            obsAvoidAlgo()

        else:
            turnRight()
            distToWall = ultrasonicReading
            while distToWall - ultrasonicReading < 5:
                moveForward()
            
            turnLeft()
            obsAvoidAlgo()
        
    if finishLineDitected == True:
        stop()
        return 0