import serial
import time
import numpy as np
import cv2
import math

class AimControl:

#https://circuitdigest.com/microcontroller-projects/rs485-serial-communication-between-arduino-and-raspberry-pi


    def aim(targetDict,img,status):

        height, width, channels = img.shape
        # Center of frame
        center_frame_x = int(width/2)+5
        center_frame_y = int(height/2)+50

        def vectorLength(x0,y0,x,y):
            return math.sqrt(math.pow((x-x0),2) + math.pow((y-y0),2))

        closestAim = dict()
        closestAim.update({
            "x": 999,
            "y": 999,
            "w": 999,
            "h": 999
        })

        # Iterate trough list of subjects and find the closest
        for key, value in targetDict.items():

            dictX = closestAim["x"]
            dictY = closestAim["y"]
            dictW = closestAim["w"]
            dictH = closestAim["h"]
            dict_center_x = int(dictX+dictW/2)
            dict_center_y = int(dictY+dictH/2)

            valueX = value[0]
            valueY = value[1]
            valueW = value[2]
            valueH = value[3]
            value_center_x = int(valueX+valueW/2)
            value_center_y = int(valueY+valueH/2)

            if (vectorLength(center_frame_x,center_frame_y,value_center_x,value_center_y) < vectorLength(center_frame_x,center_frame_y,dict_center_x,dict_center_y)):
                print('close target found')
                print(vectorLength(center_frame_x,center_frame_y,value_center_x,value_center_y))
                print(vectorLength(center_frame_x,center_frame_y,dict_center_x,dict_center_y))
                closestAim.update({
                    "x": valueX,
                    "y": valueY,
                    "w": valueW,
                    "h": valueH
                })
                print(closestAim)
        
        x = closestAim["x"]
        y = closestAim["y"]
        w = closestAim["w"]
        h = closestAim["h"]


        # Center of face rect
        center_x = int(x+w/2)
        center_y = int(y+h/2)

        cv2.line(img,(center_x-15,center_y),(center_x,center_y),(0,0,255),2)
        cv2.line(img,(center_x+15,center_y),(center_x,center_y),(0,0,255),2)
        cv2.line(img,(center_x,center_y-15),(center_x,center_y),(0,0,255),2)
        cv2.line(img,(center_x,center_y+15),(center_x,center_y),(0,0,255),2)

        # Just for illustrating purposes
        cv2.circle(img,(center_frame_x,center_frame_y), 10, (0,255,0), -1)
        cv2.rectangle(img,(center_frame_x-15, center_frame_y-15),(center_frame_x+15, center_frame_y+15),(0,255,0),3)
        cv2.line(img,(center_frame_x,center_frame_y),(center_x,center_y),(0,255,0),3)


        def inSight():
            # check if subject is in sight
            if (center_frame_x-15 < center_x < center_frame_x+15 and center_frame_y-15 < center_y < center_frame_y+15):
                # In sight
                return 1
            else:
                # Not in sight
                return 0

        def fire():
            #time.sleep(1000)
            #ardu= serial.Serial('/dev/ttyACM0',9600, timeout=.1)
            #time.sleep(1)
            #ardu.write('f'.encode())
            #ardu.close()
            print('fireeeeee')
            


        while (1):
            if (inSight()==1):
                #Fire shot
                if (status!=1):
                    fire()
                break
            elif(inSight()!=1):

                if (center_frame_x < center_x):
                    # Turn right
                    #print('right')
                    range_right = math.fabs(center_x-center_frame_x)
                    #print(range_right)
                elif (center_frame_x > center_x):
                    #Turn left
                    #print('left')
                    range_left = math.fabs(center_x-center_frame_x)
                    #print(range_left)
                if (center_frame_y < center_y):
                    # Turn down
                    #print('down')
                    range_down = math.fabs(center_y-center_frame_y)
                    #print(range_down)
                elif (center_frame_y > center_y):
                    # Turn up
                    #print('up')
                    range_up = math.fabs(center_y-center_frame_y)
                    #print(range_up)
                break
        