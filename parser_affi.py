"""
    数据解析模块,功能：
    1. 解析爬取到的源数据
    2. 增加语言信息
"""

import json
from settings import *
import os

# 获得国家-语言对照表
def get_country2language_table():
    if os.path.exists(dict_country2language_path):
        return json.load(open(dict_country2language_path))

    import openpyxl
    wb = openpyxl.load_workbook(xlsx_country2language_path)
    sheet = wb.active

    dict_c2l = dict()
    for i in range(2, sheet.max_row + 1):
        country = sheet['A%s' % i].value.replace("\xa0", '').strip(" ")
        language = sheet['B%s' % i].value
        dict_c2l[country] = language

    return dict_c2l


def paser_affi_dict(affi_dict):
    dict_res = dict()
    if affi_dict["status"] != "OK":
        return dict_res

    dict_c2l = get_country2language_table()
    location = affi_dict["results"][0]
    address_components = location.setdefault('address_components', [])
    for c in address_components:
        # 获得国家名称, 记录下来
        if "country" in c['types']:
            country = c['long_name']
            dict_res['country'] = country
            dict_res['language'] = dict_c2l.setdefault(country, "")
            break
        else:
            # 否则， 国家置为空
            dict_res['country'] = ""
            dict_res['language'] = ''


        geometry = location.setdefault('geometry', [])
        if geometry is not []:
            dict_res['la'] = geometry['location']['lat']
            dict_res['lo'] = geometry['location']['lng']

    return dict_res


if __name__ == '__main__':
    import os
    for filename in os.listdir(dir_loc_path):
        js = json.load(open(os.path.join(dir_loc_path, filename), encoding="utf-8"))
        print(filename, paser_affi_dict(js))
