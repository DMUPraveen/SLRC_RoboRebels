from controller  import Robot
r = Robot()
m1 = r.getDevice("right_finger_motor")
m2 = r.getDevice("left_finger_motor")
timestep = int(r.getBasicTimeStep())

while r.step(timestep) != -1:
    #arm.collectbox(WAIST_VAL,shoulder_val,elbow_val,wrist_val,pitch_val)
    #arm.hangbox()
    #arm.putinback(-11,0,0,0,0)
    m1.setPosition(-0.5)
    m2.setPosition(0.5)

    