from lineFollowingAlgoFuntions import junctionDetected, deadEnd, turnLeft90, turn180, leftPathPresent, poddakMoveForward, moveForward, destinationDetected, halt

def lineFollowingAlgo():
    while not junctionDetected() and not deadEnd() and not destinationDetected():
        moveForward()
        yield

    if junctionDetected():
        poddakMoveForward()
        if leftPathPresent():
            turnLeft90()

        else: 
            pass

        if destinationDetected():
            halt()
            return 0
        
    
        if deadEnd():
            turn180()



            