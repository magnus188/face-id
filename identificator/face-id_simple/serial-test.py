import serial
import time

ser = serial.Serial('COM13', baudrate = 9600, timeout = 1)

time.sleep(1.66)
print(ser.portstr)
ser.write(b'f')      
ser.close()       