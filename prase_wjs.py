# -*- coding:utf-8 -*-

import urllib
import requests
import codecs
import json
import time
from pymongo import MongoClient

'''
    网络请求
'''
def do_request(url, data, header = {}, proxies = {}):

    count = 0
    while(count < 3):
        try:
            resp = requests.post(url, data = data, headers = header, proxies = proxies)
            html = resp.text.encode("utf-8")
            return html
        except Exception as e:
            print e
            count = count + 1
            time.sleep(1)
            continue
    return None

#mongodb 数据库配置
user = "user"
password = urllib.quote_plus("password")
db_name = "db"
collection_name = "crawer"

uri = "mongodb://" + user + ":" + password + "@host:port/" + db_name + "?authMechanism=SCRAM-SHA-1"
client = MongoClient(uri)

db = client[db_name]
collection = db[collection_name]

url = "https://www.wjs.com/web/product/dataList"

for series in range(0,3):

    post_data={
        "series": series,
        "rows": "6",
        "page": "1"
    }

    data_response = do_request(url, post_data)
    json_data = json.loads(data_response)

    #增加series字段
    json_data["series"] = series
    # print json_result
    result = collection.insert(json_data)
    #休息3秒
    time.sleep(3)
