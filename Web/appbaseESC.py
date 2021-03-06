#!/usr/bin/env python

'''
File:         appbaseESC.py
Authors:      Shripal Rawal / Timothy Parks / Georden Grabuskie
Emails:       rawalshreepal000@gmail.com / parkstimothyj@gmail.com / ggrabuskie@csu.fullerton.edu
Description:  This file is specially designed to run Cerium on the Runt platform
'''


import rospy, serial, subprocess, sys
from mobility_topic.msg import joystick
from sensor_msgs.msg import Joy


# To import packages from different Directories
rootDir = subprocess.check_output('locate TitanRover2019 | head -1', shell=True).strip().decode('utf-8')
sys.path.insert(0, rootDir + '/build/resources/python-packages')
from pysaber import DriveEsc
#from lights import Rover_Status_Lights


# Instantiating The Class Object For PySabertooth
wheels = DriveEsc(128, "mixed")
armMix = DriveEsc(129, "notMixed")

#global variables
armAttached = False

try:
    # For 433 Mhz Communication
    #/dev/serial/by-id/usb-Silicon_Labs_Rover433_0001-if00-port0
    #rf_uart = serial.Serial('/dev/serial/by-id/usb-Silicon_Labs_Rover433_0001-if00-port0', 19200, timeo$
    pass
except:
    print("433 Not Connected")
    sleep(3)

def getRF():
    pass

def putRF():
    pass

def mobile(data):
    global armAttached
    try:
        print(int(data.axes[1]),int(data.axes[0]))
        wheels.driveBoth(int(data.axes[1]),int(data.axes[0]))
    except:
        print("Mobility-main-drive error")

def main(data):
    global throttle, armAttached
    if(data.buttons[3] and throttle < 1):
        throttle += .1
    if(data.buttons[1] and throttle > .3):
        throttle -= .1
    try:
        wheels.driveBoth(int(throttle*127*data.axes[1]),int(throttle*127*data.axes[0]))
        #print('Wheels = ',int(throttle*127*data.axes[1]), ' ' , int(throttle*127*data.axes[0]))
        #print('Arm    = ',int(127*data.axes[2]), ' ' ,int(127*data.axes[3]))
        armMix.driveBoth(int(127*data.axes[2]),int(127*data.axes[3]))
        #led.update(msg.mode.mode)
        if armAttached:
            #moveJoints([data.arm.J1, data.arm.J4, data.arm.J51, data.arm.J52])
            if outVals[-1] != '4':
                armMix.driveBoth(data.arm.J2, data.arm.J3)
            else:
                armMix.driveBoth(-data.arm.J3, data.arm.J3)
    except:
        print("Mobility-main-drive error")

if __name__ == '__main__':
    try:
        rospy.init_node('talker_base_mobility', anonymous=True)
        msg = joystick()
        if len(sys.argv) == 1:
            rospy.Subscriber("joy/0", Joy, main)
        else:
            rospy.Subscriber("joy/0", Joy, mobile)
        rospy.spin()
    except(KeyboardInterrupt, SystemExit):
        rospy.signal_shutdown()
        raise
