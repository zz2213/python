import requests
from threading import Timer
import datetime


# 打印时间

def send(url, title, mes):
    sendUrl = "https://api.day.app/" + url + "/" + title + "/" + mes
    requests.get(sendUrl)
    

def func():
    now = datetime.datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))


def task(s):
    now = datetime.datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    Timer(s, func, ()).start()


"""
task(10)
now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
"""
# ding
send("RYXFHftgRhq5BsomYwEb5J", "QQ", "hello")
send("pNoymLM2BzphdPd4qAoc2a", "QQ", "hello")


# getVouchersList("08", "cd141686-2664-463b-b345-30a13650fd45")
