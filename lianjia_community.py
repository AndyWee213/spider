#!/usr/bin/env python
# encoding: utf-8

import requests
import json
from bs4 import BeautifulSoup
from openpyxl import Workbook
import global_constant


def get_content(html, sheet, row_number_excel):
    soup = BeautifulSoup(html, 'html.parser')
    community_list = soup.find_all('li', attrs={'class': 'xiaoquListItem'})

    for item in community_list:
        row_number_excel = row_number_excel + 1
        name_location = 'A%s' % row_number_excel
        price_location = 'B%s' % row_number_excel
        sheet[name_location] = item.find('div', attrs={'class': 'title'}).text
        sheet[price_location] = item.find('div', attrs={'class': 'totalPrice'}).text

    next_page_div = soup.find('div', attrs={'class': 'contentBottom'})
    page_data = next_page_div.find('div', attrs={'class': 'house-lst-page-box'})['page-data']
    current_page_num = json.loads(page_data)['curPage']
    total_page = json.loads(page_data)['totalPage']
    return current_page_num != total_page and int(current_page_num) + 1 or None, row_number_excel


def get_html(url_prefix, item, page_num, sheet, row_number_excel):
    header = {
        'Host': "hz.lianjia.com",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Accept-Encoding': "gzip, deflate, sdch",
        'Accept-Language': "zh-CN,zh;q=0.8",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
        'Connection': "keep-alive"}
    while page_num is not None:
        print('开始获取' + item[1] + '区小区列表第' + str(page_num) + '页信息')
        url = url_prefix + item[0] + '/pg' + str(page_num)
        html = requests.get(url, headers=header).content.decode('utf-8')
        page_num, row_number_excel = get_content(html, sheet, row_number_excel)


def get_communities_of_hangzhou():
    for item in global_constant.counties_of_hangzhou.items():
        excel_name = item[1] + '.xlsx'
        wb = Workbook()
        ws = wb.active
        ws.title = item[1]
        url_prefix = 'https://hz.lianjia.com/xiaoqu/'
        get_html(url_prefix, item, 1, ws, 0)
        wb.save(filename=excel_name)


if __name__ == '__main__':
    get_communities_of_hangzhou()
