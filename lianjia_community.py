#!/usr/bin/env python
# encoding: utf-8

import requests
import json
from bs4 import BeautifulSoup
from openpyxl import Workbook
import global_constant

header = {
    'Host': "hz.lianjia.com",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate, sdch",
    'Accept-Language': "zh-CN,zh;q=0.8",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
    'Connection': "keep-alive"}


def get_content(html, sheet, row_number_excel):
    soup = BeautifulSoup(html, 'lxml')
    community_list = soup.find_all('li', attrs={'class': 'xiaoquListItem'})

    for item in community_list:
        row_number_excel = row_number_excel + 1
        name_location = 'A%s' % row_number_excel
        price_location = 'B%s' % row_number_excel
        time_location = 'C%s' % row_number_excel
        type_location = 'D%s' % row_number_excel
        fee_location = 'E%s' % row_number_excel
        service_company_location = 'F%s' % row_number_excel
        building_company_location = 'G%s' % row_number_excel
        building_count = 'H%s' % row_number_excel
        room_count = 'I%s' % row_number_excel
        sheet[name_location] = item.find('div', attrs={'class': 'title'}).text
        sheet[price_location] = item.find('div', attrs={'class': 'totalPrice'}).text

        detail_url_prefix = 'https://hz.lianjia.com/xiaoqu/'
        community_id = item['data-id']
        detail_url = detail_url_prefix + community_id
        detail_soup = BeautifulSoup(get_html(detail_url), 'lxml')
        community_info_list = detail_soup.find_all('div', attrs={'class': 'xiaoquInfoItem'})
        for community_item in community_info_list:
            label = community_item.find('span', attrs={'class': 'xiaoquInfoLabel'}).text
            content = community_item.find('span', attrs={'class': 'xiaoquInfoContent'}).text
            if label == '建筑年代':
                sheet[time_location] = content
            elif label == '建筑类型':
                sheet[type_location] = content
            elif label == '物业费用':
                sheet[fee_location] = content
            elif label == '物业公司':
                sheet[service_company_location] = content
            elif label == '开发商':
                sheet[building_company_location] = content
            elif label == '楼栋总数':
                sheet[building_count] = content
            elif label == '房屋总数':
                sheet[room_count] = content

    next_page_div = soup.find('div', attrs={'class': 'contentBottom'})
    page_data = next_page_div.find('div', attrs={'class': 'house-lst-page-box'})['page-data']
    current_page_num = json.loads(page_data)['curPage']
    total_page = json.loads(page_data)['totalPage']
    return current_page_num != total_page and int(current_page_num) + 1 or None, row_number_excel


def get_list_html(url_prefix, item, page_num, sheet, row_number_excel):
    while page_num is not None:
        print('开始获取' + item[1] + '区小区列表第' + str(page_num) + '页信息')
        url = url_prefix + item[0] + '/pg' + str(page_num)
        html = get_html(url)
        page_num, row_number_excel = get_content(html, sheet, row_number_excel)


def get_html(url):
    return requests.get(url, headers=header).content.decode('utf-8')


def get_communities_of_hangzhou():
    for item in global_constant.counties_of_hangzhou.items():
        excel_name = item[1] + '.xlsx'
        wb = Workbook()
        ws = wb.active
        ws.title = item[1]
        url_prefix = 'https://hz.lianjia.com/xiaoqu/'
        get_list_html(url_prefix, item, 1, ws, 0)
        wb.save(filename=excel_name)


if __name__ == '__main__':
    get_communities_of_hangzhou()
