from controller import Robot,PositionSensor
from ArmController  import armcontroll
TIME_STEP=64

class Positions:
    def __init__(self,robot: Robot,armcontroller:armcontroll):
        self.robot=robot
        self.TIME_STEP=64

        self.pitch=armcontroller.pitch_motor.getPositionSensor()
        self.wrist=armcontroller.wrist_motor.getPositionSensor()
        self.elbow=armcontroller.elbow_motor.getPositionSensor()
        self.shoulder=armcontroller.shoulder_motor.getPositionSensor()
        self.waist=armcontroller.waist_motor.getPositionSensor()


        ### Create an exception if motors are NONE
        if(self.pitch is  None):
            raise Exception("Pitch position sensor is not available")
        if(self.wrist is  None):
            raise Exception("Wrist position sensor is not available")
        if(self.elbow is  None):
            raise Exception("Elbow position sensor is not available")
        if(self.shoulder is  None):
            raise Exception("Shoulder position sensor is not available")
        if(self.waist is  None):
            raise Exception("PWaist position sensor is not available")
        
        ######### Enable-> Sensors
        self.pitch.enable(TIME_STEP)
        self.wrist.enable(TIME_STEP)
        self.elbow.enable(TIME_STEP)
        self.shoulder.enable(TIME_STEP)
        self.waist.enable(TIME_STEP)

        ########### Calling Fingers
        self.right_finger=armcontroller.finger_motor_right.getPositionSensor()
        self.left_finger=armcontroller.finger_motor_left.getPositionSensor()


        if(self.right_finger is  None):
            raise Exception("Right_Finger position sensor is not available")
        if(self.left_finger is  None):
            raise Exception("Left position sensor is not available")
        

        ######### Enble -> Sensors
        self.right_finger.enable(TIME_STEP)
        self.left_finger.enable(TIME_STEP)

    def positionvalues(self):
        waist_val=self.waist.getValue()
        shoulder_val=self.shoulder.getValue()
        elbow_val=self.elbow.getValue()
        wrist_val=self.wrist.getValue()
        pitch_val=self.pitch.getValue()
        arr=[waist_val,shoulder_val,elbow_val,wrist_val,pitch_val]
        # print(arr)
        return arr

    def isPositioned(self):
        arr=self.positionvalues()
        real_values=[-11,0.5,2.2,0,0.15]

        # print(arr,real_values)
        for realv,arrv in zip(real_values,arr):
            if arrv is None:
                return False
            if abs(arrv-realv)>0.1:
                return False
        return True
    
    def isCaught(self):
        right_val=self.right_finger.getValue()
        left_val=self.left_finger.getValue()
        arr=[right_val,left_val]
        real_values=[-1,1]
        print(arr,real_values)
        for realv,arrv in zip(real_values,arr):
            if arrv is None:
                return False
            if abs(arrv-realv)>0.9:
                return False
        return True
    
    def isHung(self):
        arr=self.positionvalues()
        real_values=[-11,0,0,0,0]

        # print(arr,real_values)
        for realv,arrv in zip(real_values,arr):
            if arrv is None:
                return False
            if abs(arrv-realv)>0.05:
                return False
        return True
    
    def isPlaced(self):
        arr=self.positionvalues()
        real_values=[-11,-0.8,-1,0,-1.3]

        # print(arr,real_values)
        for realv,arrv in zip(real_values,arr):
            if arrv is None:
                return False
            if abs(arrv-realv)>0.05:
                return False
        return True
    