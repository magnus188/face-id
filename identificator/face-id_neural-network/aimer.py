from pyfirmata import Arduino, util
import cv2

class AimControl:

    #PORT NAME: EG. COM3
    #board = Arduino('COM3')
    #iterator = util.Iterator(board)

#FIXME: What if two persons?
    def aim(x,y,w,h,frame):
        # Aiming method here
        # NB! This aims for head center
        x_coordinate = int((2*x+w)/2)
        y_coordinate = int((2*y+h)/2)
    
        #cv2.circle(frame, (x_coordinate,y_coordinate), 2, (255,0,0), thickness=3)
        
        # Draw cross
        cv2.line(frame,(int(x_coordinate-(w/15)),y_coordinate),(x_coordinate,y_coordinate),(0,0,255),2)
        cv2.line(frame,(int(x_coordinate+(w/15)),y_coordinate),(x_coordinate,y_coordinate),(0,0,255),2)
        cv2.line(frame,(x_coordinate,int(y_coordinate-(h/15))),(x_coordinate,y_coordinate),(0,0,255),2)
        cv2.line(frame,(x_coordinate,int(y_coordinate+(h/15))),(x_coordinate,y_coordinate),(0,0,255),2)