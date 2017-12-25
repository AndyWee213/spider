#!/usr/bin/env python
# encoding: utf-8

from mongoengine import *
import datetime


class Page(Document):
    title = StringField(max_length=200, required=True)
    date_modified = DateTimeField(default=datetime.datetime.now)


if __name__ == '__main__':
    connection = connect('lsl', host='172.28.128.3', port=27017)
    page = Page('Title')
    page.save()
