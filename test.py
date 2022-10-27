from urllib.request import urlopen

myURL = urlopen("https://www.runoob.com/")
# 读取一行内容
print(myURL.readline())
print("hello world")