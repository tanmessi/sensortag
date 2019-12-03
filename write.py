import codecs
file = codecs.open("numphone.py", "w", "utf-8")
print("Moi ban nhap so dien thoai moi: ")

a = input()
b= "a="
c =b+'"'+a+'"'
file.write(c);

# Đóng file
file.close()
