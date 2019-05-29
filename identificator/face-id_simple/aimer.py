import serial
import time
import numpy as np
import cv2
import math

class AimControl:

#https://circuitdigest.com/microcontroller-projects/rs485-serial-communication-between-arduino-and-raspberry-pi


    def aim(x,y,w,h,img,status):
        # Initialize arduino communication
        arduino = serial.Serial('COM13', 9600)

        # Get properties of image
        height, width, channels = img.shape

        # Center of frame
        center_frame_x = int(width/2)+5
        center_frame_y = int(height/2)+50

        # Center of face roi
        center_x = int(x+w/2)
        center_y = int(y+h/2)

        # Aiming cross
        cv2.line(img,(center_x-15,center_y),(center_x,center_y),(0,0,255),2)
        cv2.line(img,(center_x+15,center_y),(center_x,center_y),(0,0,255),2)
        cv2.line(img,(center_x,center_y-15),(center_x,center_y),(0,0,255),2)
        cv2.line(img,(center_x,center_y+15),(center_x,center_y),(0,0,255),2)

        # Just for illustrating purposes
        cv2.circle(img,(center_frame_x,center_frame_y), 10, (0,255,0), -1)
        cv2.rectangle(img,(center_frame_x-15, center_frame_y-15),(center_frame_x+15, center_frame_y+15),(0,255,0),3)
        cv2.line(img,(center_frame_x,center_frame_y),(center_x,center_y),(0,255,0),3)


        # check if subject is in sight
        def inSight():
            if (center_frame_x-15 < center_x < center_frame_x+15 and center_frame_y-15 < center_y < center_frame_y+15):
                # In sight
                return 1
            else:
                # Not in sight
                return 0

        # Fire
        def fire():
            arduino.write((b'f'))
            print((b'f'))
            #print('fireeeeee')
            #time.sleep(1000)

  
        #Aim and/or engage target
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
        