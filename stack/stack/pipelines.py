# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from logging import Logger, fatal, log
import logging

from scrapy.exceptions import DropItem
from scrapy.settings.default_settings import LOG_LEVEL
from stack.settings import MONGODB_COLLECTION, MONGODB_DB, MONGODB_PORT, MONGODB_SERVER
from itemadapter import ItemAdapter
import pymongo
from scrapy import selector, settings



class StackPipeline:
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):
    # construction function to initialize the class by defining
    # the mongo settings and then connecting to the database.
    def __init__(self):
        connection = pymongo.MongoClient(
            settings[MONGODB_SERVER],
            settings[MONGODB_PORT]
        )

        db = connection[settings[MONGODB_DB]]

        self.collection = db[settings[MONGODB_COLLECTION]]

        #Now we need to define method to process the parsed data
    def process_item(self,item,spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            Logger.info("Question added to MongoDB database",
            LOG_LEVEL=Logger.debug,spider=spider)
        return item


