#goi dien thoai
import RPi.GPIO as GPIO
import serial 
import time,sys

SERIAL_PORT = "/dev/ttyS0"
ser = serial.Serial(SERIAL_PORT,baudrate = 9600, timeout=5)

ser.write("ATD+84978912207;\r")
print("Dialing ...")
time.sleep(10) #goi 10s
ser.write("ATH\r")
print("Hanging up ...")

