from pyfirmata import Arduino, util

class AimControl:

    #PORT NAME: EG. COM3
    #board = Arduino('COM3')
    #iterator = util.Iterator(board)

#FIXME: What if two persons?
    def aim(x,y,w,h):
        # Aiming method here
        # NB! This aims for head center
        x_coordinate = (2*x+w)/2
        y_coordinate = (2*y+h)/2
        print(x_coordinate, y_coordinate)