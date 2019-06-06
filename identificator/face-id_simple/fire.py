import serial
import time

class FireControl:

    def fire():
        ser = serial.Serial('COM13', baudrate = 9600, timeout = 1)
        
        time.sleep(1.66)
        # Initialize arduino communication
        ser.write(b'f')
        ser.close()
        print('fireeeeee')