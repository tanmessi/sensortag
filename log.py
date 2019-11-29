from sim800ll import SIM800L
sim800ll=SIM800L('/dev/ttyS0')
sms="Have fall detection in home"
phone='0793931601'
#sim800l.send(dest.no,sms)
sim800ll.send_sms(phone,sms)
sim800ll.call(phone)