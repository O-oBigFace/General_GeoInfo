"""
    爬取模块: 主要的函数为spiderToList,根据一个机构列表爬取地理位置信息
"""
import json
import requests
import os
from settings import *
from Logger import logger
import warnings
warnings.filterwarnings("ignore")


__GOOGLE_KEY = "AIzaSyDDzBNqMLO96aIRbNh18LqnVeagfJK1-s8"
__HOST_lo_la = "https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key=" + __GOOGLE_KEY
__HOST_loc = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key=" + __GOOGLE_KEY
__MAX_TRY = 6


def toCountry(keys):
    # construct the url
    if type(keys) in {list, tuple}:
        url = __HOST_lo_la.format(keys[0], keys[1]) # la lo
    else:
        url = __HOST_loc.format(keys.replace(" ", "+")) # place name
    resp = requests.get(url, proxies=get_proxy(), verify=False)

    if resp.status_code == 200:
        return resp.text
    if resp.status_code == 503:
        raise Exception('Error: {0} {1}'.format(resp.status_code, resp.reason))
    else:
        raise Exception('Error: {0} {1}'.format(resp.status_code, resp.reason))


"""
    模块：get地理位置信息，保存到文件中。
"""
def sp_with_try(keys, file_res_path):
    k = keys if type(keys) in {str} else k[0]
    if os.path.exists(file_res_path):
        logger.info("EXISTED -------------%s loc info has existed-------------" % k)
        return ""
    have_try = 0
    while have_try < __MAX_TRY:
        try:
            have_try += 1
            loc_info =  toCountry(keys)
            with open(file_res_path, "w", encoding="utf-8") as fw:
                fw.write(loc_info)
            logger.info("DONE -------------%s loc info done-------------" % k)
            return loc_info
        except Exception as e:
            logger.error("%s | %s" % (k, str(e)))
    return ""


def default_item_process(i):
    if type(i) in {str}:
        return i, i
    else:
        return i, " ".join(list(i))


"""
    通用模块：给定一个可迭代的对象，爬取地理位置信息。
    需要传入一个对象处理函数:对每个迭代对象，生成一个keys和一个文件名
"""
def spiderToList(affi_list, method_item_process=default_item_process):
    import multiprocessing as mlp
    pool = mlp.Pool()

    for item in affi_list:
        keys, file_name = method_item_process(item)
        file_name = os.path.join(dir_loc_path, file_name)
        pool.apply_async(sp_with_try, args=(keys, file_name,))

    pool.close()
    pool.join()

if __name__ == '__main__':
    # al = ["china pharmaceutical university", "southeast university"]
    import pickle
    al = pickle.load(open(pkl_affi_wangfang_path, "rb"))
    spiderToList(al)
