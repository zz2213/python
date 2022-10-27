import requests

kw = {"tagId": 9, "memberName": "", "current": 1, "size": 10}

url = "https://api.banksteel.com/gateway/banksteel-riskmanage-bcs/bcs/v2/tags/tagId/member-scores"
response = requests.post(url, json=kw)
# print(response.json)
getParam = {
    "originalIdListString": "1,2"
    }
getUrl = "https://api.banksteel.com/gateway/banksteel-finance-invoice/foreign/input/record/item"
getResponse = requests.get(getUrl, params= getParam)
print(getResponse.text)