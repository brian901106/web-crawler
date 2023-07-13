import requests
from bs4 import BeautifulSoup
from datetime import datetime

headers = {
    "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6"
}

elem = []
for page_num in range(1,10):
    res = requests.get("https://www.setn.com/Klist.aspx?PageGroupID=1&ProjectID=9967&PageType=6"+"&p={}".format(page_num), headers=headers)
    soup = BeautifulSoup(res.text,"lxml")
    elem += soup.select(".newsimg-area-item-2")

total = 0
title_list = []
date_list = []

for e in elem:
    total += 1
    title_list += [title.text for title in e.select(".newsimg-area-text-2 ")]
    date_list += [date.text for date in e.select(".newsimg-date")]


datetime_object_list = []
time_interval_list = []
total_time_interval = 0
for num in range(0,total):
    print("-------------------\n"+"{} | {} | {} \n".format(str(num), title_list[num], date_list[num]))
    #print("{} \n".format(date_list[num][6:11]))
    datetime_object = datetime.strptime(date_list[num], '%m/%d %H:%M')
    datetime_object_list.append(datetime_object)

    if(num!=0):
        time_interval = (datetime_object_list[num-1]-datetime_object_list[num]).total_seconds()
        time_interval_list.append(time_interval)
        total_time_interval += time_interval

        hour, minute = int(time_interval / 3600), int(time_interval % 3600 / 60)
        print("發文間隔:{}小時{}分鐘\n".format(hour, minute))

average_time_interval = total_time_interval / (total)
hour, minute = int(average_time_interval / 3600), int(average_time_interval % 3600 / 60)
print("-------------------\n"+"平均發文間隔:{}小時{}分鐘 共{}篇\n".format(hour, minute, total))
print("最後發文時間{}\n".format( datetime_object_list[0].strftime("%m/%d %H:%M")))
total_time_interval += time_interval