import time
import os
from threading import Thread
from math import sqrt
import numpy as np
from bluepy.sensortag import SensorTag
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from sim800l import SIM800L

Rlimit = 1.2
dtime = 4.0

flag = False
sflag = False
MLmode = False
Mflag = False
countdown = dtime
email_recv = 'cristianphamle@gmail.com' # mail người nhận
phone = '0793931601'
mess = 'Falling detected ' # nội dung
sms='Have fall detection in home'
    
def control(): # bảng điều khiển
    global flag, MLmode, Mflag, Rlimit, dtime, countdown, email_recv, phone
    while True:
        while sflag:
            if flag:
                input()
                flag = False
                time.sleep(0.2)
                input('  Stopped\n  Enter to continue...')
            
            os.system('clear')
            print('\t << FALLING DETECTION >>')
            print('  [1] Start')
            print('  [2] Setting')
            print('  [0] Exit')
            
            flag = False
            countdown = dtime
            Mflag = False
            
            ctrl = input('  Your choice: ')
            if(ctrl == '1'):
                while True:
                    os.system('clear')
                    print('\t << FALLING DETECTION >>')
                    print('  < CHOOSE MODE >')
                    print('  [1] Rule mode')
                    print('  [2] ML mode')
                    print('  [0] Back')
                    ctrl = input('  Your choice: ')
                    if(ctrl == '0'):
                        break
                    elif(ctrl == '1'):
                        MLmode = False
                        flag = True
                        print('Starting Rule mode...')
                        time.sleep(2)
                        break
                    elif(ctrl == '2'):
                        MLmode = True
                        flag = True
                        print('Starting ML mode...')
                        time.sleep(2)
                        break
                    else:
                        input('>> Wrong choice! \n  Enter to try again...')
                
            elif(ctrl == '2'):
                while True:
                    os.system('clear')
                    print('\t << FALLING DETECTION >>')
                    print('  < SETTING >')
                    print('  [1] Change Rlimit. Current: ', Rlimit)
                    print('  [2] Change Receiver email. Current: ', email_recv)
                    print('  [3] Change Phone number. Current: ', phone)
                    print('  [4] Change Delay time. Current: ', dtime)
                    print('  [0] Back')
                    ctrl = input('  Your choice: ')
                    if(ctrl == '0'):
                        break
                    elif(ctrl == '1'):
                        Rlimit = float(input('  >> (Recommend 1.0 < x < 5.0) Rule-limit-value = '))
                        input('Changed. \n  Enter to continue...')
                    elif(ctrl == '2'):
                        email_recv = input('  >> Receiver email: ')
                        input('Changed. \n  Enter to continue...')
                    elif(ctrl == '3'):
                        phone = input('  >> Phone number: ')
                        input('Changed. \n  Enter to continue...')
                    elif(ctrl == '4'):
                        dtime = float(input('  >> (Recommend 3.0 < x < 10.0) Delay-time-value = '))
                        input('Changed. \n  Enter to continue...')
                    else:
                        input('>> Wrong choice! \n  Enter to try again...')
                
            elif(ctrl == '0'):
                print('Exiting...')
                time.sleep(1)
                exit()
            else:
                input('>> Wrong choice! \n  Enter to try again...')
                
    
def send_mess(): # hàm đếm ngược gửi tin nhắn
        global Mflag, countdown, dtime
        print("\n>>>> Message will be send within", round(countdown, 1), "second(s)")
        if(round(countdown, 1) == 0.0):
            ''' code gửi tin nhắn/mail đặt ở đây'''
            sendsms()
            send_mail()           
            print("\t<< Message sent. >>")
            Mflag = False
            countdown = dtime
            time.sleep(3)
        countdown -= 0.2
        round(countdown, 1)
def sendsms():
    sim800l=SIM800L('/dev/ttyS0')
    sim800l.send_sms(phone,sms)

def send_mail():
    global email_recv
    email_user = 'letanpham0208@gmail.com'#tai khoan dang nhap
    email_password = 'Letan@123'#pass
    
    subject = 'Detected-Falling Alert' # tiêu đề thư
    time_tuple = time.localtime()
    body = mess + time.strftime('%H:%M:%S  %d/%m/%Y', time_tuple) # nội dung
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_recv
    msg['Subject'] = subject

    msg.attach(MIMEText(body,'plain'))
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email_user,email_password)


    server.sendmail(email_user,email_recv,text)
    server.quit()

class SensorTagCollector(Thread):

    def __init__(self, device_mac, sampling_interval_sec=0.5, retry_interval_sec=5):

        Thread.__init__(self)
        self.daemon = True
        self.tag = None
        self.device_mac = device_mac
        self._sampling_interval_sec = sampling_interval_sec
        self._retry_interval_sec = retry_interval_sec
        # Connects with re-try mechanism
        self._re_connect()
        self.start()

    def _connect(self):
        """
        Connects with a SensorTag Device.
        :return: None
        """
        os.system('clear')
        print ('PREPARING...\nConnecting to SensorTag...', end='')
        self.tag = SensorTag(self.device_mac)
        print (' connected.')
        time.sleep(1)
        self._enable()

    def _enable(self):
        """
        Enables accelerometer sensors.
        :return: None
        """
        # Enabling selected sensors
        self.tag.accelerometer.enable()
        # Some sensors (e.g., temperature, accelerometer) need some time for initialization.
        print ('Enabled accelerometer sensors.')
        time.sleep(1)
    
    def run(self):
        """
        Prints values read from each sensor from a single SensorTag Device.
        In case of a dis-connectivity, it tries to re-connect automatically.
        :return: None
        """
        global flag, MLmode, Mflag, Rlimit, sflag
        
        # load model
        print('Getting model...', end='')
        model = load_model('models/md1.h5')
        print(' ML mode is ready!\nDONE!')
        time.sleep(1.5)
        
        # inverse label to string
        lb = LabelEncoder()
        lb.fit(['nan', 'stand', 'sit', 'lie', 'walk', 'fall'])
        
        # file to save data
        file = open ("data.csv","a")
        if (os.path.getsize("data.csv")==0):
            file.write("AccX,AccY,AccZ,Pred")
        
        # comput vars
        Xml = np.full((9, 3), 0.0)
        Xr = [0, 0, 0]
        X, Y, Z = [0, 0, 0], [0, 0, 0], [0, 0, 0]

        tm = 0
        count = 0
        temp = []
        show = []
        
        sflag = True
        
        while True:
            while True:
                try:
                    # đọc dữ liệu từ sensor
                    x, y, z = self.tag.accelerometer.read()
                    
                    #xử lý để dán nhãn cho MLmode
                    Xml = np.delete(Xml, 0, 0)
                    Xml = np.concatenate((Xml, [[x, y, z]]), axis=0)
                    
                    # xử lý để dự đoán cho Rmode
                    del X[0]
                    del Y[0]
                    del Z[0]
                    X.append(x)
                    Y.append(y)
                    Z.append(z)
                    del Xr[0]
                    A = sqrt(abs(max(X)-min(X))*abs(max(X)-min(X))+abs(max(Y)-min(Y))*abs(max(Y)-min(Y))+abs(max(Z)-min(Z))*abs(max(Z)-min(Z)))
                    Xr.append(A)
                    value = max(Xr) - min(Xr)
                    
                    # phần dự đoán
                    if(MLmode): # cho máy học
                        rs = str(lb.inverse_transform([[np.argmax(model.predict(np.array([Xml])))]])[0])
                    else: # cho Rule
                        if (value >= Rlimit):
                            rs = 'fall'
                        else:
                            rs = 'normal'
                    
                    # phần hiển thị
                    if(flag==True):
                        if(MLmode):
                            show.append([rs, round(x,4), round(y,4), round(z,4)])
                        else:
                            show.append([rs, round(value,4), round(x,4), round(y,4), round(z,4)])
                        if(len(show) >= 20): # 20 là số dòng tín hiệu được hiển thị
                            del show[0]
                        
                        os.system('clear')
                        print('\t << FALLING DETECTION >>')
                        for sh in show:
                            print(sh)
                        
                        print('\nMode:','ML mode' if(MLmode) else 'Rule mode')
                        
                        # nếu có 2 fall liên tục thì đếm ngược gửi tin nhắn (cho Rule)
                        if (rs == 'fall'):
                            print("\n  << Warning: Falling Detect! >>")
                            count += 1
                            if(count >= 2):
                                if(not(MLmode)):
                                    Mflag = True
                                    count = 0
                        # ML mode: nếu có >= 2 fall và ít nhất 3 lie hoặc >= 5 fall thì cảnh báo
                        if(count == 1):
                            if(rs != 'fall'):
                                count = 0
                        if(count != 0):
                            if(count <= 10):
                                temp.append(rs)
                            else:
                                if(temp.count('lie') >= 3 or temp.count('fall' >= 5)):
                                    Mflag = True
                                    count = 0
                            count += 1
                        
                        if(Mflag):# đếm ngược gửi tin nhắn
                            send_mess()
                        print('  << Press Enter to stop >>')
                            
                    else:
                        show = []
                        Mflag = False
                        countdown = dtime
                        count = 0
                            
                    tm += 0.2
                    
                    file.write("\n")
                    file.write(str(x)+","+str(y)+","+str(z)+","+str(rs))
                    self.tag.waitForNotifications(self._sampling_interval_sec)
                
                except Exception as e:
                    print (str(e))
                    self.tag.disconnect()
                    break

            time.sleep(self._retry_interval_sec)
            self._re_connect()
    
    def _re_connect(self):
        """
        Reconnects with a SensorTag Device
        :return:
        """
        while True:
            try:
                self._connect()
                break
            except Exception as e:
                print (str(e))
                time.sleep(self._retry_interval_sec)


if __name__ == '__main__':
    SensorTagCollector(device_mac="24:71:89:BF:0B:84", sampling_interval_sec=0.2)
    Thread(target=control).start()
    