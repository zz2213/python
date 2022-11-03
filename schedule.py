from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import requests
import time


class my_CronTrigger(CronTrigger):
    # def __init__(self, year=None, month=None, day=None, week=None, day_of_week=None, hour=None,
    #              minute=None, second=None, start_date=None, end_date=None, timezone=None,
    #              jitter=None):
    #     super().__init__(year=None, month=None, day=None, week=None, day_of_week=None, hour=None,
    #              minute=None, second=None, start_date=None, end_date=None, timezone=None,
    #              jitter=None)
    @classmethod
    def my_from_crontab(cls, expr, timezone=None):
        values = expr.split()
        if len(values) != 7:
            raise ValueError('Wrong number of fields; got {}, expected 7'.format(len(values)))

        return cls(second=values[0], minute=values[1], hour=values[2], day=values[3], month=values[4],
                   day_of_week=values[5], year=values[6], timezone=timezone)


def times():
    print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))


# token
tokenEnum = {
    "zhao": "068b022b-5b77-4d06-97fc-3b5c3f35b77f",
    "ding": "-5b77-4d06-97fc-3b5c3f35b77f",

}

# bark推送key
barkEnum = {
    "ding": "RYXFHftgRhq5BsomYwEb5J",
    "zhao": "pNoymLM2BzphdPd4qAoc2a"

}


vouchersEnum = {
    # 5元消费券
    5: "6228127c62ff4125c690ea50",
    # 10元消费券
    10: "6228149062ff4125c690ea51",
    # 20元消费券
    20: "6228153462ff4125c690ea52",
    # 30元消费券
    30: "622815b562ff4125c690ea53",
    50: "62299598fceddb10cd1cb64d",
    80: "6229976ffceddb10cd1cb64f"
}


def getHour():
    hour = time.localtime().tm_hour
    if hour > 8 and hour < 12:
        return "12"
    elif hour > 12 and hour < 18:
        return "18"
    else:
        return "08"


def send(url, title, mes):
    sendUrl = "https://api.day.app/" + url + "/" + title + "/" + mes
    requests.get(sendUrl)


# 获取消费券列表
def getVouchersList(period, token):
    url = "https://mapv2.51yundong.me/api/coupon/stocks?view=&groupId=common&time=" + period + "%3A00&noHaveCode=true"
    authorization = "Bearer "+token
    headers = {
       "Host": "mapv2.51yundong.me",
       "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.29(0x18001d30) NetType/4G Language/zh_CN",
       "Connection": "keep-alive",
       "Authorization": authorization,
       "Accept-Encoding": "gzip,compress,br,deflate",
       "Referer": "https://servicewechat.com/wx8b97e9b9a6441e29/176/page-frame.html",
       "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.get(url, headers=headers)
    return response.status_code


# 抢消费券
def rushVouchers(stockId, period, token):
    url = "https://mapv2.51yundong.me/api/coupon/coupons/send?stockId="+stockId+"&time="+period+"%3A00"
    authorization = "Bearer "+token
    headers = {
       "Host": "mapv2.51yundong.me",
       "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.29(0x18001d30) NetType/4G Language/zh_CN",
       "Connection": "keep-alive",
       "Authorization": authorization,
       "Accept-Encoding": "gzip,compress,br,deflate",
       "Referer": "https://servicewechat.com/wx8b97e9b9a6441e29/175/page-frame.html",
       "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.get(url, headers=headers)
    return response.status_code


"""
1.先获取抢购消费券场次 08 12 18
2.获取消费券列表 判断token是否正确
3.调用抢购消费券

"""


def rush(user, price):
    period = getHour()
    listCode = getVouchersList(period, tokenEnum.get(user))
    print(listCode)
    if listCode == 200:
        send(barkEnum.get(user), "消费券", "token正确开始抢购")
        start = time.time()*1000
        endTime = time.time()*1000
        get = 0
        while endTime-start < 6 and get != 200:
            get = rushVouchers(vouchersEnum.get(price), period, tokenEnum.get(user))
            time.sleep(0.1)
            endTime = time.time()*1000
        if get == 200:
            send(barkEnum.get(user), "消费券", "消费券已抢到")
        else:
            send(barkEnum.get(user), "消费券", "未抢到消费券")
    elif listCode == 401:
        send(barkEnum.get(user), "消费券", "token错误")
    else:
        print("token:" + str(listCode))
        send(barkEnum.get(user), "消费券", "服务器错误")


# rush("zhao")
sched = BlockingScheduler()
# sched.add_job(times, my_CronTrigger.my_from_crontab('0 14 15,8,12,18 * * * *'))
# 删除30天前的文件
# args用于函数中进行传值,可以随机命名,只需要在后面传递参数即可
sched.add_job(rush, my_CronTrigger.my_from_crontab('0 0 15,8,12,18 * * * *'), args=("zhao", 10))
# sched.add_job(func=times, trigger='cron', hour='15,3,8,12,18', minute='13')
sched.start()
