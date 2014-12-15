from datetime import datetime
import pymongo
import requests
from scrapy.exceptions import DropItem
#coding=utf-8
from dirbot import settings


class FilterWordsPipeline(object):
    """A pipeline for filtering out items which contain certain words in their
    description"""

    # put all words in lowercase
    words_to_filter = ['politics', 'religion']
    def __init__(self):
        print settings.MONGODB_URL
        conn = pymongo.Connection(settings.MONGODB_URL)
        mongodb = conn[settings.MONGODB_NAME]
        mongodb.authenticate(settings.MONGODB_USER, settings.MONGODB_PASSWORD)
        self.collection = mongodb[settings.COLLECTION]
        print self.collection.count()
    def process_item(self, item, spider):
        address = item['address']
        url = "http://api.map.baidu.com/geocoder/v2/?address="+address+"&output=json&ak=FEc72f64f2ea54c81422a833b1c4d02d"
        response = requests.get(url)
        content = eval(response.content)
        print content['result']['level']
        # location = content['result']['location']
        # param = {'name': item['name'], 'address': item['address'], "province": item['province'], 'city': item['city'], 'district': item['district'], 'location': location, 'createTime': datetime.now()}
        # self.collection.insert(param)
        return item







