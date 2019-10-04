import time
from threading import Thread
from bluepy.sensortag import SensorTag
import os

class SensorTagCollector(Thread):
   
    def __init__(self, device_mac, sampling_interval_sec=1, retry_interval_sec=5):
      
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
        print ("Connecting to SensorTag")
        self.tag = SensorTag(self.device_mac)
        print "Connected..."
        self._enable()

    def _enable(self):
        """
        Enables accelerometer sensors.
        :return: None
        """
        # Enabling selected sensors
        self.tag.accelerometer.enable()
        # Some sensors (e.g., temperature, accelerometer) need some time for initialization.
        time.sleep(1)
        print "Enabled accelerometer sensors.."

    def run(self):
        """
        Prints values read from each sensor from a single SensorTag Device.
        In case of a dis-connectivity, it tries to re-connect automatically.
        :return: None
        """
        file = open ("data.csv","a")
        if (os.path.getsize("data.csv")==0):
            file.write("AccX, AccY, AccZ, Action")
        while True:
            while True:
                try:              
                    s = self.tag.accelerometer.read()      
                    print(" Accelerometer: ",s )                    
                    self.tag.waitForNotifications(self._sampling_interval_sec)
                    file.write("\n")
                    file.write(str(s).replace("(","").replace(")",""))
                except Exception as e:
                    print str(e)
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
                print str(e)
                time.sleep(self._retry_interval_sec)


if __name__ == '__main__':

    SensorTagCollector(device_mac="24:71:89:C0:4F:01", sampling_interval_sec=1)

    while True:
        pass
