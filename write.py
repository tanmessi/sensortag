import codecs
file = codecs.open("sdt.py", "w", "utf-8")
print("Nhap noi dung file")

a = input()
b= "a="
c =b+'"'+a+'"'
file.write(c);

# Đóng file
file.close()
