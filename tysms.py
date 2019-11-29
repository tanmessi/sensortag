import RPi.GPIO as GPIO
import serial 
import time,sys

SERIAL_PORT = "/dev/ttyS0"
ser = serial.Serial(SERIAL_PORT,baudrate = 9600, timeout=5)

ser.write("AT+CMGF=1\r")
print("Text mode enable")
time.sleep(3)
ser.write('AT+CMGS="+84978912207"\r')
msg = "xin chao Ty"
time.sleep(3)
ser.write(msg+chr(26)) #ctrl+z
time.sleep(3)
print("Da gui")
