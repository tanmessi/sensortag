#goi dien thoai
import RPi.GPIO as GPIO
import serial 
#from serial import Serial
import time,sys
import numphone
numphone=numphone.a
chuoi=";\r"
SERIAL_PORT = "/dev/ttyS0"
ser = serial.Serial(SERIAL_PORT,baudrate = 9600, timeout=5)

ser.write(("ATD"+(numphone)+(chuoi)).encode())
print("Dialing ...")
time.sleep(15)
ser.write("ATH\r".encode())
print("Hanging up ...")

print("Ban co muon thay doi so dien thoai hay nhap 1, neu khong nhap 0")
a = 0
a = input()
if a == "1" :
  import write
  print("So dien thoai da thay doi")
else:
  print("Khong thay doi")

