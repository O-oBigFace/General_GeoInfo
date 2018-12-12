from settings import *
import wangfang_prepro
import spider4country
import parser_affi
import os
from Logger import logger
import json

def main():
    affi_list = wangfang_prepro.get_wangfang_affi()

    # 爬取直到无可爬
    spider_set = set(affi_list) - set(os.listdir(dir_loc_path))
    isChanged = True
    count = 1
    while spider_set and isChanged:
        logger.info("MAIN: +++++++++++++++++++++++++++++round: %d, target: %d+++++++++++++++++++++++++++++" % (count, len(spider_set)))
        spider4country.spiderToList(spider_set)
        # 更新参数
        count += 1
        new_spider_set = set(affi_list) - set(os.listdir(dir_loc_path))
        if len(spider_set) is len(new_spider_set):
            isChanged = False
        spider_set = new_spider_set

    dict_res = dict()
    for filename in os.listdir(dir_loc_path):
        js = json.load(open(os.path.join(dir_loc_path, filename), encoding="utf-8"))
        dict_res[filename] = parser_affi.paser_affi_dict(js)

    json.dump(dict_res, open(result_dict_wangfang_path, "w"))

    logger.info("+_+_+_+_+_+_+_+_+_+_+_ALL DONE_+_+_+_+_+_+_+_+_+_+_+_")

if __name__ == '__main__':
    main()
