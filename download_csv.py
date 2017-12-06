import os.path
import urllib.request
import time
import random
from datetime import timedelta, date, datetime
from dateutil.relativedelta import relativedelta

start_dt = date(2017, 11, 30)
end_dt = date(2017, 12, 4)


def date_range(date1, date2):
    n = 0
    while date1 + timedelta(n) <= date2:
        yield date1 + timedelta(n)
        n = n + 1


def month_range(date1, date2):
    n = 0
    while date1.replace(day=1) + relativedelta(months=n) <= date2.replace(day=1):
        yield date1.replace(day=1) + relativedelta(months=n)
        n = n + 1


def download_data(_url, _path):
    if not os.path.exists(_path):
        urllib.request.urlretrieve(_url, _path)
        print("........downloaded at " + datetime.now().time().strftime("%H:%M:%S"))
        time.sleep(random.uniform(1, 10))

# FMTQIK 每日市場成交資訊
print("========FMTQIK========")
for dt in month_range(start_dt, end_dt):
    print(dt.strftime("%Y%m%d"))
    url = "http://www.twse.com.tw/exchangeReport/FMTQIK?response=csv&date=" + dt.strftime("%Y%m%d")
    path = "/home/olycats/github/twse/FMTQIK/" + dt.strftime("%Y%m%d") + ".csv"
    download_data(url, path)

# MI_5MINS 每5秒委託成交統計
print("========MI_5MINS========")
for dt in date_range(start_dt, end_dt):
    print(dt.strftime("%Y%m%d"))
    url = "http://www.twse.com.tw/exchangeReport/MI_5MINS?response=csv&date=" + dt.strftime("%Y%m%d")
    path = "/home/olycats/github/twse/MI_5MINS/" + dt.strftime("%Y%m%d") + ".csv"
    download_data(url, path)

# MI_5MINS_INDEX 每5秒委託成交統計
print("========MI_5MINS_INDEX========")
for dt in date_range(start_dt, end_dt):
    print(dt.strftime("%Y%m%d"))
    url = "http://www.twse.com.tw/exchangeReport/MI_5MINS_INDEX?response=csv&date=" + dt.strftime("%Y%m%d")
    path = "/home/olycats/github/twse/MI_5MINS_INDEX/" + dt.strftime("%Y%m%d") + ".csv"
    download_data(url, path)


