# import requests
from threading import Timer
import datetime

"""
 kw = {"tagId": 9, "memberName": "", "current": 1, "size": 10}

url = "https://api.banksteel.com/gateway/banksteel-riskmanage-bcs/bcs/v2/tags/tagId/member-scores"
 response = requests.post(url, json=kw)
 print(response.json)
"""

"""
getParam = {
    "originalIdListString": "4090761,4090759"
    }
getUrl = "https://api.banksteel.com/gateway/banksteel-finance-invoice/foreign/input/record/item"
getResponse = requests.get(getUrl, params=getParam)
print(getResponse.text)
"""

# ¥Ú”° ±º‰


def func():
    now = datetime.datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))


def task(s):
    now = datetime.datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    Timer(s, func, ()).start()


task(10)
now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
